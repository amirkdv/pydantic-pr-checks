# Pydantic PR Checks

A Github Action for enforcing PR guidelines, primarily for [pydantic].

[pydantic]: https://github.com/samuelcolvin/pydantic

## Quick Start

To use this action:

```yaml
on:
  pull_request:
    types: [opened, reopened, edited]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: amirkdv/pydantic-pr-checks@v1.0
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          repo: ${{ github.repository }}
          number: ${{ github.event.number }}
```

Alternatively, for better performance, you can use the pre-built Docker image
published on [dockerhub]:

```yaml
steps:
  - uses: docker://amirkdv/pydantic-pr-checks:v1.0
    with:
      token: ${{ secrets.GITHUB_TOKEN }}
      repo: ${{ github.repository }}
      number: ${{ github.event.number }}
```

[dockerhub]: https://hub.docker.com/repository/docker/amirkdv/pydantic-pr-checks/

## Checks

1. PR title does not reference issue IDs
2. A `Change Summary` section exists.
3. A `Related issue number` section exists, referencing an issue with a proper
   linking verb like "fixes".
4. A `Checklist` section exists and all tasks in it are complete.
5. A `changes/[number]-[user].md` file is included, briefly describing the change.

## Development

To get started:

```sh
(venv) $ make install
(venv) $ make test
(venv) $ make lint
```

If you want to directly debug the main script:
```
(venv) $ INPUT_TOKEN=... INPUT_REPO=... INPUT_NUMBER=... ./main.py
```

**Note**: To avoid mistakes, the `main.py` script prints failing checks to
stdout instead of posting a Github comment. To post a comment, use:

```sh
(venv) $ main.py --action comment
```

### Docker

Docker is only used to speed up the usage in Github actions. You do not need
docker for normal development and testing.

Docker image workflow:

```sh
# assumes the latest tag is locally present, if not: git pull --tags
$ make docker-build
$ make docker-test
$ make docker-publish
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
