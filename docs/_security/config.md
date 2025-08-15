---
layout: page
title: Config
---

The Flask app configuration is defined by `config.py`, which contains 3 classes.

The Config class is the base class for two different configurations.

## Config

### Secret Key

This pulls the crytpographic key from `.env` which signs session cookies, CSRF tokens, etc.

### Permanent Session Lifetime

Sets a time limit on how long session keys last before they expire, prompting the user to login again. Right now it is set to 5 minutes.

### Session Permanent

This is a flag for if session keys should expire. With it set to `False`, session data will never expire, so when the site goes live this will be changed to `True`.

### WTF CSRF Enabled

Enables CSRF protection for Flask-WTF forms.

### Session & Remember Cookie Samesite

Adds the SameSite attribute to cookies, which dictates what site origins are accepted when the server recieves a request. This prevents another server from using cookies from this website to make a request to another website.

If this wasn't here, another server could hijack a user's cookies and make a request as that user, which is obviously not good.

`Lax` blocks cross-site POST requests containing our cookies, but allows top-level navigation, meaning being redirected to a page not requiring cookies or authorization.


### Session & Remember Cookie Secure

Marks cookies as secure, requiring they are sent over HTTPS _only_. This is overwritten in `DevConfig` to make development easier by not requiring HTTPS for every page.


### Session & Remember Cookie HTTP Only

Prevents any javascript from reading session cookies. This forces any script trying to access this sensitive information to go through pre-defined internal functions.

---

## RedisConfig

### Redis URL

Defines the URL for the local redis server. This is the same as connecting to a database.

### Session Type

Tells Flask we are using redis as our session storage

### Session Redis

Creates a redis client from the URL. `decode_responses=False` tells redis to store information as bytes which is useful since our encryption functions take bytes.

### Session Key Prefix

Every session key that is stored in Redis will have "sess:" in front of it. Not necessary if the only thing ever stored in redis is session keys, but if we ever want to store more information, we can set different prefixes to prevent key collisions.

### Session Use Signer

Signs the session ID cookie with a unique key when it is stored, and checks that key when it is pulled to prevent tampering while not in transit.

### Session Refresh Each Request

On each request, the TTL (time to live) for the redis session key will be refreshed.

---

## DevConfig

### Session Type

Sets session data to be stored on your local system to make development easier. This is __not__ secure and should absolutely __not be used in production__. Always use redis for actual deployments.

### Session Cookie Secure

Set this to false to make development easier.

### Session File Dir

Tells Flask where to store session data on your machine. With this config it will be stored in the root project directory under a folder titled `.flask_session`.
