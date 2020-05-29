from brutemark.parser import TokenizeLine
from brutemark.line_tokens import OrderedItemLine, UnorderedItemLine

ordered_line = "123. Hello World"
nested_ordered_line = "  123. Hello World"

unordered_line = "* Hello World"
nested_unordered_line = "  * Hello World"


def test_ordered_line_items():
    tokenized_line = TokenizeLine(ordered_line)

    assert isinstance(tokenized_line, OrderedItemLine)
    assert tokenized_line.nested == 0

    tokenized_line = TokenizeLine(nested_ordered_line)
    assert isinstance(tokenized_line, OrderedItemLine)
    assert tokenized_line.nested == 2


def test_unordered_line_items():
    tokenized_line = TokenizeLine(unordered_line)
    assert isinstance(tokenized_line, UnorderedItemLine)
    assert tokenized_line.nested == 0

    tokenized_line = TokenizeLine(nested_unordered_line)
    assert isinstance(tokenized_line, UnorderedItemLine)
    assert tokenized_line.nested == 2