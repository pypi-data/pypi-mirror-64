SQLAlchemy Qubole
==============================

The `SQLAlchemy <https://docs.sqlalchemy.org>`_ is the Python SQL Toolkit and Object Relational Mapper. The primary purpose of this is to have a working dialect for Qubole Presto and Hive that can be used with `Apache Superset <https://superset.incubator.apache.org>`_. This uses Qubole JDBC driver to connect to Qubole Presto/Hive.

Prerequisites
-------------

* JDK 8 or later
* Python 3.x

Installation
------------

* Download the Qubole JDBC driver (version 2.3 or later) from `here <https://docs.qubole.com/en/latest/connectivity-options/use-qubole-drivers/JDBC-driver/download-jdbc-driver.html>`_
* Set the environment variable QUBOLE_JDBC_JAR_PATH pointing to JDBC JAR location with absolute path

Example:

    ::

        export QUBOLE_JDBC_JAR_PATH=/Users/testuser/qubolejdbc/qds-jdbc-2.3.0.jar

* Install the sqlalchemy-qubole package. The package is available on `PyPI <https://pypi.python.org/pypi/sqlalchemy-qubole>`_

  ::

    $ pip install sqlalchemy-qubole

Note: Ensure pip is pointing to Python3 OR use pip3 instead as this package supports Python 3.x version

Example of SQLAlchemy URIs to connect to Qubole
-----------------------------------------------

* Presto Dialect:

  ::

    qubole+presto://presto/presto_cluster?endpoint=https://api.qubole.com;password=<API-TOKEN>;catalog_name=hive

* Hive Dialect:

  ::

    qubole+hive://hive/hadoop2?endpoint=https://api.qubole.com;password=<API-TOKEN>

* Default Dialect: By default, Qubole dialect points to presto.

  ::

    qubole://presto/presto_cluster?endpoint=https://api.qubole.com;password=<API-TOKEN>;catalog_name=hive

Reporting Bugs
--------------

* Want to report a bug or request a feature? Please contact `Qubole Support <https://www.qubole.com/services-support/technical-support>`_.