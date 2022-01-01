import pytest
from ..markdown import MarkdownDocument


def deindent(string):
    lines = string.split('\n')

    indentation = -1
    for line in lines:
        if not line:
            continue
        indentation = len(line) - len(line.lstrip(' '))
        break

    assert indentation >= 0

    out = ''
    for line in lines:
        assert not line or line[:indentation] == ' ' * indentation, f"Unexpected indentation: {line}"
        out += '\n' + line[indentation:]

    return out


def run(string):
    md = MarkdownDocument(deindent(string))
    sections = md.sections_by_title()
    return {
        # str(e) produces the HTML markup for the element
        title: ''.join(str(e) for e in body).strip()
        for title, body in sections.items()
    }


def test_single_section():
    sections = run("""
    # Title

    Body
    """)
    assert len(sections) == 1
    assert 'Title' in sections
    assert sections['Title'].strip() == '<p>Body</p>'


def test_two_sections():
    sections = run("""
    # Title 1

    Body 1

    # Title 2

    Body 2
    """)
    assert len(sections) == 2
    assert sections['Title 1'] == '<p>Body 1</p>'
    assert sections['Title 2'] == '<p>Body 2</p>'


def test_two_sections_different_depth():
    sections = run("""
    # Title 1

    Body 1

    ## Title 2

    Body 2
    """)
    assert len(sections) == 2
    assert sections['Title 1'] == '<p>Body 1</p>'
    assert sections['Title 2'] == '<p>Body 2</p>'


def test_two_sections_same_title():
    with pytest.raises(ValueError):
        run("""
        # Title 1

        Body 1

        ## Title 1

        Body 2
        """)


def test_empty_body():
    sections = run("""
    # Title 1

    Body 1

    ## Title 2
    """)

    assert len(sections) == 2
    assert sections['Title 2'] == ''


def test_leading_content():
    sections = run("""
    Ignored content

    # Title

    Body
    """)

    assert len(sections) == 1
    assert sections['Title'] == '<p>Body</p>'
