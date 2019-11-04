from brutemark.parser import TokenizeLine
from brutemark.line_tokens import OrderedItemLine, UnorderedItemLine

def test__line_tokens__OrdereredItemLine__testconsume_detects_ordered_items_correctly():

    normal_test = "123. Hello World"
    expected = OrderedItemLine("Hello World", False)
    _, actual = OrderedItemLine.TestAndConsume(normal_test)

    assert actual is not None
    assert actual.content == expected.content
    assert actual.nested is False

    nested_test = "  123. Hello World"
    expected = UnorderedItemLine("Hello World", True)
    _, actual = UnorderedItemLine.TestAndConsume(nested_test)

    assert actual.content == expected.content
    assert actual.nested is True



def test__line_tokens__UnorderedItemLine__testconsume_detects_unordered_items_correctly():

    normal
