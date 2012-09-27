from setuptools import setup

setup(
    name='btrc',
    version='1.0',
    description='Couchbase view btree stats collector',
    author='Pavel Paulau',
    author_email='pavel.paulau@gmail.com',
    scripts=['btrc'],
    install_requires=['requests'],
    setup_requires=[],
    tests_require=[],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
