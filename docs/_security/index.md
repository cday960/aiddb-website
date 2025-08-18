---
layout: page
title: Overview
nav_order: 1
---

# Security Overview

Information on all the security implementations from nonce to fernet.

## Config

`config.py` is how we define settings and build options for the flask app. There is a base `Config` class which sets settings for everything besides how session data is stored.

Then that base class is extended to make `RedisConfig` and `DevConfig`.

`RedisConfig` sets the app to use a redis server to store session data. This will be the production configuration.

`DevConfig` sets the app to store session data in a folder in the root project directory. This is not secure, even if all data stored is encrypted, so it is only used when running the app locally for development.

Read more about the [Config Setup]({{ site.baseurl }}{% link _security/config.md %})

## Encryption

We are using the `Fernet` module from the included `cryptography` library for encryption.

Fernet utilizes a generated secret key to encrypt and decrypt data. This secret key is stored in the `.env` file.

The only file Fernet is used in is `util/crypto_utils.py`. For more information about how encryption is handled, read [crypto_utils.py]({{ site.basurl }}{% link _file_details/util.md %}).

## Content Secure Policy (CSP)

A CSP is a set of headers that are attached to every response object the server sends out. These headers tell the browser to place restrictions on what the website can actually do, for example restricting images from being loaded from an external url. Read more on [Content Secure Policy Headers]({{ site.baseurl }}{% link _security/csp.md %}).

## Nonce

A nonce (number used once) is a randomly generated string that is attached to the response objects CSP headers that prevents script injection attacks.

### Lifecycle of a Nonce

1. Server receives a request.
2. A new nonce is generated and attached to the response.
3. Server receives new request on the same endpoint triggering a script.
4. Check new request to see if the nonce that was generated is attached to the script. If not, the script is external and will be blocked.

## Authentication

All authentication is done through the SQL server aiddb. 

The login page takes db login info, then attempts to establish a connection. If it succeeds, the login info is encrypted and stored in the session data. If it fails, nothing is stored and the user must attempt to login again. See [custom_sql_class.py]({{ site.basurl }}{% link _file_details/util.md %}) for more info.

This logic is implemented with decorators. Read [decorators]({{ site.baseurl }}{% link _guide/decorators.md %}) for more information.

## Forms

All user data input is handled through `Flask-WTF` forms, a library that implements [WTForms](https://wtforms.readthedocs.io/en/3.2.x/) into Flask and Python. It lets us create classes that automatically sanitize and constrain inputted data before it is used in the backend. See [forms]({{ site.baseurl }}{% link _guide/forms.md %}) for more information.
