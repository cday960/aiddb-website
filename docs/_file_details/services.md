---
layout: page
title: Services
nav_order: 5
---

# Services
Files in this folder contain utility functions that need to access flask session data or connect to the database.

## `db_service.py`
This is a wrapper for functions in `dao/mssql_dao.py`.

Right now it only contains `list_people()`, which calls the `get_top_people()` function from the dao.

That's it. It is just a strongly typed wrapper function file for db access.

## `session_db.py`
This file is where any function that connects to the db and uses session data should live.

Right now it only has one, very important, function `get_db()`. This is how the database object should be initialized within view functions.
