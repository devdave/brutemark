from brutemark.parser import Blocker, TokenizeBody, TokenizeLine
from brutemark.line_tokens import HTMLLine, CodeLine

test_document = """<table>
    <tr>
        <td>Hello</td>
        <td>World</td>
    </tr>
</table>"""

def test_htmlline_correctly_consumes_the_correct_line_and_ignores_tabbed_or_spaced_lines():
    """
    raw html lines cannot be tabbed/spaced to avoid mixing them up with CodeLine's
    """
    _, actual = HTMLLine.TestAndConsume("<span>")
    assert actual is not None
    assert isinstance(actual, HTMLLine)

    _, actual = HTMLLine.TestAndConsume("   <dd>")
    assert actual is not None
    assert isinstance(actual, HTMLLine)

    _, actual = HTMLLine.TestAndConsume("   <dt bar=\"123\">")
    assert actual is not None
    assert isinstance(actual, HTMLLine)

    _, actual = HTMLLine.TestAndConsume("<dt bar=\"123\">")



def test_tokenize_line_recognizes_html():
    blocks = Blocker(test_document)

    for block in blocks:
        for line in block:
            product = TokenizeLine(line)
            assert isinstance(product, (HTMLLine, CodeLine,))