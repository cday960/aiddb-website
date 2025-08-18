---
layout: page
title: DAO
nav_order: 1
---

# Data Access Object

## Purpose

This file contains isolated, frequently used queries that are used to display information on pages from the database.

## Isolation

This file never accesses the database or flask session data directly. So if one of these queries fails or its behavior changes, we know the issue is with the query itself and not the database connection or auth process.

## Function Arguments

All functions in this file are ___strongly typed___, including the return type, to make implementation easier.

Every function takes a db object, which should be initialized using
```
db = get_db()
```
