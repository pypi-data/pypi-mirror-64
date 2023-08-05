# curlylint [![Travis](https://travis-ci.com/thibaudcolas/curlylint.svg?branch=master)](https://travis-ci.com/thibaudcolas/curlylint) [![Total alerts](https://img.shields.io/lgtm/alerts/g/thibaudcolas/curlylint.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/thibaudcolas/curlylint/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/thibaudcolas/curlylint.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/thibaudcolas/curlylint/context:python)

A prototype linter which checks the indentation and the correctness of
[Jinja](http://jinja.pocoo.org/docs/2.9/)-like/HTML templates. Can [fix issues](https://github.com/django/djangoproject.com/commit/14a964d626196c857809d9b3b492ff4cfa4b3f40).

It works with [Django’s templates](https://docs.djangoproject.com/en/1.11/ref/templates/language/) too, it should
work with [Twig](https://twig.symfony.com/) and similar template languages.
It should work fine with any kind of HTML 4 and 5, however XHTML is not
supported.

This linter parses both HTML and Jinja tags and will report mismatched
tags and indentation errors:

```html+jinja
<div>
  {% if something %}
</div>
{% endif %}
```

```html+jinja
<div>
    <span>
    </div>
</span>
```

```html+jinja
{% if something %}
<div>not indented properly</div>
{% endif %}
```

```html+jinja
{% if something %}<a href="somewhere"
  >{% endif %}
  <p>something</p>
  {% if not something %}</a
>{% endif %}
```

## Usage

You need Python 3. Curlylint doesn’t work with Python 2. Install it with
`pip install curlylint` (or `pip3 install curlylint` depending on how `pip` is
called on your system), then run it with:

```sh
curlylint template-directory/
```

…or:

```sh
curlylint some-file.html some-other-file.html
```

This is a work in progress. Feel free to contribute :upside_down_face:

### CLI flags

#### `--verbose`

Turns on verbose mode. This makes it easier to troubleshoot what configuration is used, and what files are being linted.

```sh
curlylint --verbose template-directory/
```

#### `--parse-only`

Don’t lint, check for syntax errors and exit.

```sh
curlylint --parse-only template-directory/
```

### Configuration

Curlylint supports defining a config file with the flag `--config`. Here is an [example config](./example_config.py) file with the available options:

```python
# Specify additional Jinja elements which can wrap HTML here. You
# don't need to specify simple elements which can't wrap anything like
# {% extends %} or {% include %}.
# Default: [].
jinja_custom_elements_names = [
    ('cache', 'endcache'),
    ('captureas', 'endcaptureas'),
    # ('for', 'else', 'empty', 'endfor'),
]

# How many spaces to use when checking indentation.
# Default: 4
indent_size = 4
```

This config file can then be used with:

```sh
curlylint --config example_config.py template-directory/
```

## Usage with [pre-commit](https://pre-commit.com) git hooks framework

Add to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/thibaudcolas/curlylint
  rev: "" # select a tag / sha to point at
  hooks:
    - id: curlylint
```

Make sure to fill in the `rev` with a valid revision.

_Note_: by default this configuration will only match `.jinja` and `.jinja2`
files. To match by regex pattern instead, override `types` and `files` as
follows:

```yaml
- id: curlylint
  types: [file] # restore the default `types` matching
  files: \.(html|sls)$
```

## Hacking

Curlylint is powered by [Parsy](https://github.com/python-parsy/parsy). Parsy is an extremely powerful
library and curlylint’s parser relies heavily on it. You have to read
Parsy’s documentation in order to understand what’s going on in
`parse.py`.
