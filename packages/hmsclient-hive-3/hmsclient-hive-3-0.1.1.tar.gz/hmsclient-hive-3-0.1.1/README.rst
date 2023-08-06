HMSClient For Hive Metastore API version 3.0
============================================

This repo is just a rebuild of @gglanzani great work here: https://github.com/gglanzani/hmsclient.
All I have done is to regenerate the code according to the authors instructions (below).
After installing all the prereqs, the command ran to regenerate the code was:

.. code-block:: shell
    
    python generate.py --metastore_url https://raw.githubusercontent.com/apache/hive/branch-3.0/standalone-metastore/src/main/thrift/hive_metastore.thrift
    
Below: the original writers notes


This project aims to be an up to date Python client to interact with the Hive metastore
using the Thrift protocol.

Installation
------------

Install it with ``pip install hmsclient-hive-3`` or directly from source

.. code-block:: python

    python setup.py install

Usage
-----

Using it from Python is simple:

.. code-block:: python

    from hmsclient import hmsclient
    client = hmsclient.HMSClient(host='localhost', port=9083)
    with client as c:
        c.check_for_named_partition('db', 'table', 'date=20180101')


Regenerate the Python thrift library
------------------------------------

The ``hmsclient.py`` is just a thin wrapper around the generated Python code to
interact with the metastore through the Thrift protocol.

To regenerate the code using a newer version of the ``.thrift`` files, you can
use ``generate.py`` (note: you need to have ``thrift`` installed, see here_)

.. code-block:: sh

    python generate.py --help

    Usage: generate.py [OPTIONS]

    Options:
      --fb303_url TEXT      The URL where the fb303.thrift file can be downloaded
      --metastore_url TEXT  The URL where the hive_metastore.thrift file can be
                            downloaded
      --package TEXT        The package where the client should be placed
      --subpackage TEXT     The subpackage where the client should be placed
      --help                Show this message and exit.

Otherwise the defaults will be used.

.. _here: https://thrift-tutorial.readthedocs.io/en/latest/installation.html
