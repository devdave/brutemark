from lxml.html.builder import E
from lxml.html import tostring
from brutemark.markdown import markdown

def test_inline_HTML():

    test = \
"""
<table>
    <tr>
        <td>Foo</td>
    </tr>
</table>
"""

    expected = E("table",
                    E("tr",
                        E("td", "Foo")
                    )
    )
    expected_str = tostring(expected, pretty_print=True, encoding="unicode")

    actual = markdown(test)
    assert actual == expected_str