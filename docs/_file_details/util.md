---
layout: page
title: Util
nav_order: 8
---

# Util
This folder contains util files that are used throughout the flask app. These files are responsible for providing important services which is why it is outside of the app folder.

## crypto_utils.py

Contains the encrypt and decrypt functions for storing and pulling the user's password from flask session data.

To encrypt/decrypt a string using Fernet, it must first be converted into bytes, then once it is encrypted/decrytped converted back to a string.

I made these two helper functions to ensure that a view function doesn't accidentally use the bytes version of a password.

## custom_sql_class.py

Class file that automatically builds a database object using `pyodbc`.

This db object will automatically open a connection and connect to it, disconnect when not being used, and close the connection when the db object goes out of scope.

### connect()
This method establishes a connection to the database.

It first detecs what system the flask app is running on. This is for development, as once it is deployed the correct SQL driver will not change. But for right now on Windows it needs to use the SQL Server driver, while Linux (WSL) needs to use FreeTDS.

Then, depending on which OS it detects, it will define the connection string and use the given username, password, server, and database.

The default server is "aiddb", and default database is "Columbia". If no server and db are given then it will use the defaults.

If the connection fails a `ConnectionError` is raised which will get caught by the `requires_login` decorator and flash the error message on the screen. If the connection succeeds, then that connection is set to the connection attribute of the object.

### close()
Closes the connection and logs the event.

### query(self, query, strip, params)
This method will run a query on the database. It has error checking to guarantee that a connection is established, as well as safeguards to prevent unintended changes to the db.

__Strip__: This boolean argument tells the function if there is an extra syntax highlighting flag in the SQL query string. In my IDE, I have injections for my syntax highlighter that detects "--sql" at the beginning of a string and highlights the rest of it as SQL. Defaults to False, so unless you're using a similar plugin in your IDE, you can ignore this.


__Params__: This is a list of arguments that will be sent to `cursor.execute()` with the query. An example usage would be
```python
cursor.execute("select a from tbl where b=? and c=?", x, y)
```

### query_with_columns()
Executes a query and returns a tuple of type
```python
(rows: List[pyodbc.Row], columns: List[str])
```
So you can easily pull the headers out of the result.


### query_dicts()
Executes a query, using `query_with_columns()`, but instead of returning a tuple it returns a list of dictionaries.

Each dictionary in the list is a row, and they key value pairs are {column_name: value}.

Example:
```python
{'personID': 123456, 'studentNumber': '123456', 'lastName': 'Smith', 'firstName': 'John'}
```
