from brutemark.parser import TokenizeBody, Text, StrongText, EmphasisText


def test_detects_strong_markdown():

    test = "Hello __world__"
    expected = [Text("Hello "), StrongText("world")]
    actual = TokenizeBody(test)

    assert isinstance(actual[0], Text)
    assert isinstance(actual[1], StrongText)


def test_detects_emphasis_markdown():

    test = "Hello _World_"
    expected = [Text("Hello "), EmphasisText("World")]
    actual = TokenizeBody(test)

    assert isinstance(actual[0], Text)
    assert isinstance(actual[1], EmphasisText)


def test_strong_nested_in_emphasis():

    test = "_Hello **World**_"
    expected = [EmphasisText([Text("Hello "),StrongText("World")])]
    actual = TokenizeBody(test)

    assert len(actual) == 1
    assert actual[0].content == expected[0].content