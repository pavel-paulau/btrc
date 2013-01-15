Prerequisites
-------------

* Python 2.6
* pip

Installation
-------------

    pip install btrc

Usage
-------------

Once you have pointed btrc to node it will collect stats from all nodes in cluster and all design docs for specified bucket:

    btrc -n 127.0.0.1:8091 -b default -c btree_stats

    btrc -n 127.0.0.1:8091 -b default -c util_stats

You also can reset utilization stats:

    btrc -n 127.0.0.1:8091 -b default -c reset
