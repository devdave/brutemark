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