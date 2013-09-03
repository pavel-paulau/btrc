#!/usr/bin/env python
import sys
import json
from optparse import OptionParser

import requests
from logger import logger


class CouchbaseClient(object):

    """Minimal Couchbase client
    """

    def __init__(self, host_port, bucket, username, password):
        self.base_url = 'http://{0}'.format(host_port)
        self.bucket = bucket
        self.auth = (username, password)

    def _get_list_of_nodes(self):
        """Yield CAPI host:port names"""
        url = self.base_url + '/pools/default/'
        try:
            r = requests.get(url=url, auth=self.auth).json()
        except requests.exceptions.ConnectionError:
            sys.exit('Cannot establish connection with specified [host:port] '
                     'node')
        if r is not None:
            for node in r['nodes']:
                hostname, port = node['hostname'].split(':')
                if port == '8091':
                    yield hostname + ':8092'
                else:
                    yield hostname + ':9500'
        else:
            sys.exit('Node has no buckets/misconfigured')

    def _get_list_of_ddocs(self):
        """Yield names of design documents in specified bucket"""
        url = self.base_url + \
            '/pools/default/buckets/{0}/ddocs'.format(self.bucket)
        try:
            r = requests.get(url=url, auth=self.auth).json()
        except ValueError:
            return []
        if r is not None:
            return (row['doc']['meta']['id'] for row in r['rows'])
        else:
            sys.exit('Wrong bucket name')

    def _gen_set_view_url(self):
        """Yield URLs for _set_view interface"""
        for node in self._get_list_of_nodes():
            for ddoc in self._get_list_of_ddocs():
                url = 'http://{0}'.format(node) + \
                      '/_set_view/{0}/{1}/'.format(self.bucket, ddoc)
                yield node, ddoc, url

    def get_btree_stats(self):
        """Yield btree stats"""
        for node, ddoc, url in self._gen_set_view_url():
            url += '_btree_stats'
            try:
                yield node, ddoc, requests.get(url=url, auth=self.auth).json()
            except requests.exceptions.ConnectionError as e:
                logger.warn(e)

    def get_utilization_stats(self):
        """Yield utilization stats"""
        for node, ddoc, url in self._gen_set_view_url():
            url += '_get_utilization_stats'
            try:
                yield node, ddoc, requests.get(url=url, auth=self.auth).json()
            except requests.exceptions.ConnectionError as e:
                logger.warn(e)

    def reset_utilization_stats(self):
        """Reset all utilization stats"""
        for _, _, url in self._gen_set_view_url():
            url += '_reset_utilization_stats'
            requests.post(url=url, auth=self.auth)


class CliArgs(object):

    """CLI options and args handler
    """

    def __init__(self):
        usage = 'usage: %prog -n node:port [-b bucket] -c command \n\n' +\
                'Example: %prog -n 127.0.0.1:8091 -u Administrator -p password -b default -c btree_stats'

        parser = OptionParser(usage)

        parser.add_option('-n', dest='host_port',
                          help='Node address', metavar='127.0.0.1:8091')
        parser.add_option('-u', dest='username',
                          help='REST username', metavar='Administrator')
        parser.add_option('-p', dest='password',
                          help='REST password', metavar='password')
        parser.add_option('-b', dest='bucket', default='default',
                          help='Bucket name', metavar='default')
        parser.add_option('-c', dest='command',
                          help='Stats command', metavar='command')

        self.options, self.args = parser.parse_args()
        self.validate_options(parser)

    def validate_options(self, parser):
        if not self.options.host_port:
            parser.error('Missing node address [-n]')
        if not self.options.command:
            parser.error('Missing command [-c]')
        if self.options.command not in ('btree_stats', 'util_stats', 'reset'):
            parser.error('Only "btree_stats", "util_stats" and "reset" '
                         'commands supported')


class StatsReporter(object):

    """Save all stats in *.json files
    """

    def __init__(self, cb):
        self.cb = cb

    def report_stats(self, stats_type):
        if stats_type == 'btree_stats':
            stats_generator = self.cb.get_btree_stats
        else:
            stats_generator = self.cb.get_utilization_stats

        for node, ddoc, stat in stats_generator():
            filename = '{0}_{1}{2}.json'.format(stats_type,
                                                node.replace(':', '_'),
                                                ddoc.replace('/', '_'))
            with open(filename, 'w') as fh:
                logger.info('Saving {0} stats to: {1}'.format(stats_type,
                                                              filename))
                fh.write(json.dumps(stat, indent=4, sort_keys=True))


def main():
    ca = CliArgs()
    cb = CouchbaseClient(ca.options.host_port, ca.options.bucket,
                         ca.options.username, ca.options.password)
    reporter = StatsReporter(cb)

    if ca.options.command in ('btree_stats', 'util_stats'):
        reporter.report_stats(ca.options.command)
    elif ca.options.command == 'reset':
        cb.reset_utilization_stats()

if __name__ == '__main__':
    main()
