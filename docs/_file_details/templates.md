---
layout: page
title: Templates
nav_order: 7
---

# Templates

This folder contains all of the html files.

## `base.html`

Every other page is an extension of this page, so any changes to this file will affect every single page on the site. This is because we are utilizing Jinja templating.

Only contains links, sources, metadata, navbar, and the flash box.

Currently, the only links are our css page in `static`, and the bootstrap css page.
The javascript sources are our static js file, and the bootstrap js file for extra frontend functionality (like the dropdown in the navbar).

### Jinja Templating
All blocks wrapped with curly braces, either double or with a percentage sign {% raw %}(so {{ ... }} or {% ... %}) {% endraw %}, are jinja template blocks.

Double curly braces are used to call injected variables, so objects passed to the `render_tempalte` function. 

Curley brace with percentage are used to do loops, set aliases, execute conditional logic, and define template blocks. Template blocks are how we use this base file with every othe file. 

In the body of `base.html` it only contains {% raw %}`{% block content %} {% endblock %}`{% endraw %}, which means that if another page extends `base.html` and then defines a block named content, that block is placed in the body of `base.html`.

The navbar is also wrapped in a jinja block, allowing a new page to either override it with a page specific navbar, or to leave the block blank, so
{% raw %}
```jinja
{% block navbar %} {% endblock %}
```
{% endraw %}

which will remove the navbar from the page, since it is replacing the existing navbar block in `base.html` with nothing.
