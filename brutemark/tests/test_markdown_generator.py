from lxml.html.builder import E
from lxml.html import tostring

import textwrap
from brutemark.markdown import markdown, ROOT_CONTAINER
from brutemark import line_tokens


def test_simple_generation_single_header():
    test = \
    textwrap.dedent("""
    # Hello World
    """).strip()

    expected = tostring(
        E("div",
            E("h1", "Hello World"),
            **{"class":"brutemark_root"}
          )
    )
    actual = markdown(test)

    assert actual == expected




def test_simple__multiline_paragraph():
    test = \
    """
    This is a test of the assembler. 
    This line should be followed by a  
    br tag
    """

    test = textwrap.dedent(test).strip()

    expected_text =\
    [
        "This is a test of the assembler. ",
        "This line should be followed by a  ",
        E("br"),
        "br tag"
    ]

    root_kwargs = {"class":"brutemark_root"}
    root = E("div", E("p", *expected_text), **root_kwargs)
    expected = tostring(root)

    actual_string = markdown(test)

    assert expected == actual_string

def test_simple_multiline_code():


    test = \
    """    This is a code block
        that spans
        multiple lines"""

    expected_text = \
    [
        "This is a code block\n",
        "that spans\n",
        "multiple lines"
    ]

    root_kwargs = {"class": "brutemark_root"}
    expected = tostring(
        E("div",
            E("pre",
                E("code", *expected_text)
            ),
            ** root_kwargs
        )
    )

    actual = markdown(test)

    assert actual == expected



def test_simple_multiple_ordered_list():
    test = "\n".join([
        "1. First item",
        "2. Second item"
    ])

    root_kwargs = {"class": "brutemark_root"}
    expected = tostring(
        E("div",
            E("ol",
                E("li", "First item"),
                E("li", "Second item")
            ),
            ** root_kwargs
        )
    )
    actual = markdown(test)

    assert actual == expected

