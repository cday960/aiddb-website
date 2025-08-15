---
layout: page
title: Content Security Policy
nav_order: 4
---

# Content Security Policy

CSP headers are essentially a whitelist, officially called directives, for what resources can be loaded, and where they can be loaded from.

They are set in `app/lib/security.py`. Here's a quick, surface level rundown of what each of these headers does.

## `default-src 'self'; `

If a resource type doesn't have its own directive, then it uses the `default-src` directive. `self` means only load resources from the _same origin_, aka the website aka scheme+host+port.


## `script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; `

Script source defines where javascript can come from.

In this case, it can be internal, `'self'`, or it can come from the url `https://cdn.jsdelivr.net'`. This cdn is whitelisted here because that is where all of the bootstrap scripts come from, which is responsible for dropdown menus, dynamic rendering, etc.

The `'nonce-{nonce}'` directive, which pulls the most recently generated nonce out of the g object (see more [here](#)) and sets it in the header allowing internal inline '<script>' blocks to run.


## `style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; `

CSS files have to be local, `'self'`, or from the jsdelivr cdn.

`'unsafe-inline'` allows inline styling and `style=""` attributes in HTML tags.


## `img-src 'self' data:; `

Images have to be local or a data URI. 


## `connect-src 'self'; `

This dictates what endpoints a script-initiated request can connect to. So since it only includes `self`, then calling an external API like `fetch('https://fake.api.com/user_list')` would fail. But calling an internal one like `fetch('/api/profile/<id>')` would work.


## `frame-ancestors 'none';`

This prevents any page from this site from being embedded.
