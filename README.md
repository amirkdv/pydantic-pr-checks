# Markdown Sections

You want to enforce structure on markdown strings, eg PR or issue bodies? This
is a library and Github Action that helps you reason about the semantic
structure of markdown strings. This helps you answer questions like:

* Does it contain a section titled `Steps to Reproduce` or `Summary of Changes`?
* Are all the tasks in `Merge Checklist` marked as complete?

## Sections

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

## How it Works

1. Markdown is parsed into HTML using [commonmark.py].
2. HTML is traversed using [beautifulsoup] to identify sections.
3. Output is all sections in HTML identified by their title.

[commonmark.py]: https://pypi.org/project/commonmark/
[beautifulsoup]: https://pypi.org/project/beautifulsoup4/

## Limitations

Sections as defined above have no awareness of the nesting relationships among
themselves. In the example above, the fact that the `Details` section is a child
of `Summary` section is lost. The output of markdown-sections is simply:

```json
{
  "Summary": "<p> Body </p> <ul> <li> some </li> <li> list </li> </ul>",
  "Details": "<p> More things </p>"
}
```

## Why not Regular Expressions?

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
