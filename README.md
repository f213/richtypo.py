# Richtypo — the only web typograph that don't make a mess out of your text

Richtypo assumes that your text already has right dashes and quotes. The main concern is to add
non-breaking spaces to the right places.

This project is heavily inspired by Artem Sapegin's [richtypo](https://github.com/sapegin/richtypo.js/).

## Features

- Blazing fast, aimed for render-time use.
- Native Russian support.
- HTML and Markdown aware, does not break your markup.
- Your text stays readable and indexable — richtypo does not produce HTML entities and other messy stuff.
- Easy integration with Jinja2, Django templates and any other language.
- Well tested Python3 and Python2 support. For py2 only unicode input is accepted.
- Easily extendable through smallest possible regular expressions defined in YAML with in-place specifications.

## Installation

```sh
pip install richtypo
```

## Usage
```python
from richtypo import Richtypo


r = Richtypo(ruleset='ru-lite')

well_done = r.richtypo(text)
```

### Jinja2 filter

```python
from richtypo.filter import filter

env = jinja2.Environment(
    filters={
        'richtypo': filter
    }
)
```

Template:

```html
{{ text | richtypo('ru-lite') }}
```

### Django filter

```python
# your_app/templatetags/richtypo.py

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from richtypo.filter import filter as typograph

register = template.Library()


@register.filter
@stringfilter
def richtypo(value, ruleset='generic'):
    return mark_safe(typograph(value, ruleset))
```

Template:
```html
{% load richtypo %}

{{ object.text | richtypo:"ru-lite"}}
```


## License

MIT