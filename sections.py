#!/usr/bin/env python3
import re
import sys
import json
import argparse
from typing import Dict

from bs4 import BeautifulSoup
from commonmark import commonmark


class UnexpectedDocFormat(Exception):
    pass


class MarkdownDocument:
    def __init__(self, body: str):
        self.body = body
        self.html = commonmark(self.body)
        self.doc = BeautifulSoup(self.html, 'html.parser')

    def sections_by_title(self) -> Dict[str, str]:
        """Extracts all sections in the body, identified by title. A section is a
        sequence of DOM siblings between any two consecutive headings.

        Raises an exception if two headings have the same text, wherever in the
        document.
        """
        headings = self.doc.select('h1, h2, h3, h4, h5, h6')

        sections = {}
        for heading in headings:
            title = heading.text.strip()
            if title in sections:
                raise ValueError(f"Body contains multiple headings '{title}'")

            sections[title] = ''
            for elem in heading.next_siblings:
                if not elem.name:
                    # text nodes
                    sections[title] += str(elem)
                    continue

                if re.match(r'h\d', elem.name):
                    # next heading
                    break

                sections[title] += str(elem)

        return sections


def main(args: argparse.Namespace) -> int:
    body = args.input.read()
    md = MarkdownDocument(body)
    print(json.dumps(md.sections_by_title(), indent=2))
    return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Runs checks against a PR description.")
    parser.add_argument('input', type=argparse.FileType('r', encoding='UTF-8'))
    args = parser.parse_args()
    sys.exit(main(args))
