
from brutemark.parser import TokenizeLine
from brutemark.line_tokens import QuotedLine

blockquote = """> Single line blockquote"""
nested_blockquote = """  > Single line blockquote that is nested"""

def test_blockquote_consumes_string_correctly():
    _, actual = QuotedLine.TestAndConsume(blockquote)

    assert actual is not None
    assert isinstance(actual, QuotedLine)
    assert actual.content == "Single line blockquote"

    _, actual = QuotedLine.TestAndConsume(nested_blockquote)
    assert isinstance(actual, QuotedLine)
    assert actual.nested == True
    assert actual.content == "Single line blockquote that is nested"


def test_detects_blockquote():
    tokenized_line = TokenizeLine(blockquote)

    assert isinstance(tokenized_line, QuotedLine)
    assert tokenized_line.nested is False


def test_blockquote_detected_and_is_nested():
    tokenized_line = TokenizeLine(nested_blockquote)

    assert tokenized_line.nested is True

