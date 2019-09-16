# pymysqlwrapper

Provides a simple API for running SQL on a MySQL datatabase.

## api

* `go` — primary function for running SQL. *See docstring for details.*
  * Takes a parameterized statement.
  * You can specify whether you'd like a single value returned, a single row, or multiple rows.

   ~~~
  go(db_spec
      ,parameterized_stmt
      ,data_tuple
      ,returnkind=ReturnKind.ALLROWS
      ,commit=False)
  ~~~


* `ReturnKind` — an enum for use with `go` to specify the shape of what `go` returns:
  * ReturnKind.SINGLEVALUE
  * ReturnKind.ONEROW
  * ReturnKind.ALLROWS
  
* `check_conn(db_spec)` — confirm your db connection is good.

### example usage

~~~
stmt = 'insert into snapshots(context, itemid, payload) values (%s, %s, %s)'
vals = ('primary', '101', 'testing 1 2 3')
rslt = go(db_spec, stmt, vals, commit=True)
print rslt # Should be an empty tuple for insert statements.
~~~

## db_spec data structure

Functions in the package take an argument called `db_spec`. It should be a map with the following key-value pairs like so:

~~~
{ "host": "localhost"
, "user": "X"
, "password": "X"
, "db": "mydb" 
, "charset": "utf8mb4" }
~~~

Optionally, add a `port` key-value pair as well.

## running check_connection.py

From the root of the project:

    mkdir enclave

In the enclave folder, make a file called `db_spec.json` containing
JSON formatted per the db_spec format described above.

Then, from the root of the project, create a virtualenv, install dependencies, and run:

    mkdir venv
    virtualenv venv
    source venv/bin/activate
    python setup.py install
    python check_connection.py

## requirements

Compatible with Python 2.7.

