from brutemark.parser import Blocker, TokenizeBody, TokenizeLine
from brutemark.line_tokens import HTMLLine

test_document = """<table>
    <tr>
        <td>Hello</td>
        <td>World</td>
    </tr>
</table>
"""


def test_tokenize_line_recognizes_html():
    blocks = Blocker(test_document)

    for block in blocks:
        for line in blocks:
            assert isinstance(line, HTMLLine)