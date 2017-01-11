# Richtypo — the only web typograph that don't make a mess out of your text

This library assumes that your text already has right dashes and quotes. The main concern is to add
non-breaking spaces to the right places.

This project is heavily inspired by Artem Sapegin's [richtypo](https://github.com/sapegin/richtypo.js/).

## Features

- Blazingly fast, aimed for realtime use.
- Native Russian support.
- HTML and Markdown aware, richtypo does not break your markup.
- Your text stays readable and indexable — richtypo does not produce HTML entities and other messy stuff.
- Easily extendable through lousely coupled small regular expressions defined in YAML.
- Well tested Python3 and Python2 support. For py2 only unicode input is accepted.

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

Or as jinja2 filter:

```python
from richtypo.filter import filter

env = jinja2.Environment(
    filters={
        'richtypo': filter
    }
)
```

```html
{{ text | richtypo('ru-lite') }}
```

## License

MIT