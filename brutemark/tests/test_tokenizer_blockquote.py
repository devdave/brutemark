
from brutemark.parser import TokenizeLine, TokenTypes, QuotedLine

blockquote = """>Single line blockquote"""
nested_blockquote = """  >Single line blockquote that is nested"""

def test_detects_blockquote():
    tokenized_line = TokenizeLine(blockquote)

    assert isinstance(tokenized_line, QuotedLine)
    assert tokenized_line.nested is False


def test_blockquote_detected_and_is_nested():
    tokenized_line = TokenizeLine(nested_blockquote)

    assert tokenized_line.nested is True

