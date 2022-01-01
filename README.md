# Pydantic PR Checks

A Github Action for enforcing PR guidelines, primarily for [pydantic].

[pydantic]: https://github.com/samuelcolvin/pydantic

## Quick Start

To use this action:

```yml
on:
  pull_request:
    types: [opened, reopened, edited]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: docker://amirkdv/pydantic-pr-checks:latest
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          repo: ${{ github.repository }}
          number: ${{ github.event.number }}
```

## Checks

ToDo

## Development

Getting started:
```sh
(venv) $ make install
(venv) $ make test
(venv) $ make lint
```

Testing the main script:
```
(venv) $ INPUT_TOKEN=... INPUT_REPO=... INPUT_NUMBER=... ./main.py
```

**Note**: this will post a comment as the owner of the access token on the given
pull request if there are any failing checks!

Building and deploying docker image:
```sh
# assumes the latest tag is locally present
$ make build
$ make push
```

## How it Works

### Sections

The key concept here is sections. They represent a semantic piece of the
document tree represented by a markdown string. A section is identified by a
heading and contains whatever comes immediately after a heading and before its
subsequent headings.

For example, in the document:
```markdown

# Summary

Body

- some
- list

## Details

More things.
```
The `Summary` section contains two elements: a `<p>` and a `<ul>`.

### Limitations

Sections as defined above have no awareness of the nesting relationships among
themselves. In the example above, the fact that the `Details` section is a child
of `Summary` section is lost.

### Why not Regular Expressions?

It's tempting to use regular expressions as a quick and dirty hack to identify
important pieces from a markdown string. Maybe markdown feels more amenable to
such hacks than [html]? It's not. Markdown is capable of producing complex DOM
structures, even we exclude the possibility of raw HTML in it.

[html]: https://stackoverflow.com/a/1732454

For example:

~~~markdown
# Heading

Some text followed by a code block:
```python
import sys

# this is a Python comment, not a markdown section
```
Or another one:
```markdown
We're now in a nested markdown block and

- [ ] this is not an incomplete task in the original document.
```
~~~
