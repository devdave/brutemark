from brutemark.parser import TokenizeBody, Text, StrongText, EmphasisText


def test_emphasis_star_is_negated_by_slash():
    leading_test = r"Hello \*world*"
    expected = Text(leading_test, 0, len(leading_test))
    actual = TokenizeBody(leading_test)

    assert len(actual) == 1
    assert isinstance(actual[0], Text)
    assert actual[0].content == leading_test

    trailing_test = r"Hello *World\*"
    expected = Text(trailing_test, 0, len(trailing_test))
    actual = TokenizeBody(trailing_test)

    assert len(actual) == 1
    assert isinstance(actual[0], Text)
    assert actual[0].content == trailing_test

    _, leading_token = EmphasisText.Consume(leading_test)
    assert leading_token is None

    _, trailing_test = EmphasisText.Consume(trailing_test)
    assert trailing_test is None



def test_emphasis_consume_matches():
    test = "Hello _World_"
    expected = EmphasisText("World",6,13)
    actual_text, actual_token = EmphasisText.Consume(test) # type: EmphasisText

    assert actual_token is not None
    assert actual_token.start == expected.start
    assert actual_token.content == expected.content
    assert actual_token.stop == expected.stop

def test_strong_consumes_match():
    test = "Hello __World__"
    expected = StrongText("World",6,15)
    actual_text, actual_token = StrongText.Consume(test)

    assert actual_token is not None
    assert actual_token.start == expected.start
    assert actual_token.stop == expected.stop
    assert actual_token.content == expected.content

def test_detects_strong_markdown():

    test = "Hello __world__"
    expected = [Text("Hello ",0,6), StrongText("world",7,13)]
    actual = TokenizeBody(test)

    assert isinstance(actual[0], Text)
    assert isinstance(actual[1], StrongText)


def test_detects_emphasis_markdown():

    test = "Hello _World_"
    expected = [Text("Hello ",0,6), EmphasisText("World",7,13)]
    actual = TokenizeBody(test)

    assert isinstance(actual[0], Text)
    assert isinstance(actual[1], EmphasisText)


def test_emphasis_consumes_nested_strongtext():
    test = "_Hello **World**_"
    expected_content = "Hello **World**"
    expected = EmphasisText("Hello **World**", 0, 17)
    actual_text, actual_token = EmphasisText.Consume(test)

    assert actual_token is not None
    assert actual_token.content == expected_content
    assert actual_token.start == expected.start
    assert actual_token.stop == expected.stop




def test_strong_nested_in_emphasis():

    test = "_Hello **World**_"
    expected = [
            EmphasisText(
                [
                    Text("Hello ",0,6),
                    StrongText("World", 0 , 7)
                ],
                0,17
            )
    ]

    actual = TokenizeBody(test)

    assert len(actual) == 1
    assert isinstance(actual[0], EmphasisText)
    assert actual[0].content[0].content == expected[0].content[0].content