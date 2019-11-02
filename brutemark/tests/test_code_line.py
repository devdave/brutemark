from brutemark.parser import TokenizeLine
from brutemark.line_tokens import CodeLine

tabbed_code ="\tA=123"
spaced_code = "    A=123"
nested_tabbed_code = "\t  A=123"
nested_spaced_code = "      A=123"


def test_detected_tabbed_codeline():
    tokenized_line = TokenizeLine(tabbed_code)
    assert isinstance(tokenized_line, CodeLine)


def test_detected_spaced_codeline():
    tokenized_line = TokenizeLine(spaced_code)
    assert isinstance(tokenized_line, CodeLine)

def test_nested_tabbed_code():
    tokenized_line = TokenizeLine(nested_tabbed_code)
    assert isinstance(tokenized_line, CodeLine)
    assert tokenized_line.nested == True

def test_nested_spaced_code():
    tokenized_line = TokenizeLine(nested_spaced_code)
    assert isinstance(tokenized_line, CodeLine)
    assert tokenized_line.nested == True