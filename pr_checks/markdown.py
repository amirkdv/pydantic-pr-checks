import re
from typing import Dict, List

from bs4 import BeautifulSoup
from commonmark import commonmark


class UnexpectedDocFormat(Exception):
    pass


class MarkdownDocument:

    def __init__(self, raw: str):
        self.raw = raw
        self.html = commonmark(self.raw)
        self.doc = BeautifulSoup(self.html, 'html.parser')

    def sections_by_title(self) -> Dict[str, List[BeautifulSoup]]:
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

            sections[title] = []
            for elem in heading.next_siblings:
                if not elem.name:
                    # text nodes
                    sections[title].append(elem)
                    continue

                if re.match(r'h\d', elem.name):
                    # next heading
                    break

                sections[title].append(elem)

        return sections
