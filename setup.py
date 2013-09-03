from setuptools import setup

setup(
    name='btrc',
    version='3.1.0',
    description='Couchbase view stats collector',
    author='Pavel Paulau',
    author_email='pavel.paulau@gmail.com',
    py_modules=['btrc'],
    entry_points={
        'console_scripts': ['btrc = btrc:main']
    },
    install_requires=[
        'logger',
        'requests==1.2.0',
    ],
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
