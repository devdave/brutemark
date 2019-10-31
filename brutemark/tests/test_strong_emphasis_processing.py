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
    """
    So this one is a bit more complicated and may cause a drastic change to the tokenizer logic.

        Nested markup creates a problem where
            MarkupA and MarkupB can inversely nest each other.

    __Foo **bar** string__ is easier based on processor precedence
    but
    *Foo __bar__ string* complicates things.

    Another problem would be goofy URLS for Anchor and Image tokens
    [Foo](http://server.tld/foo__bar__url.html "Title string")
    and
    [Foo](http://server.tld/foo_bar_url.html "Title string")
    would be caught by Strong and Emphasis body tokens which would be inappropriate

    Switching to a lower level tokenizer with
        ^__Hello **World**__ this is a link to [Markdown](link_rel "title")
    TO
        [EmphasisToken,Hello, ,StrongToken,World, ,this, ,is, ,a, ,link, ,to, ,ANCHOR_BODY,Markdown,ANCHOR_BODY,ANCHOR_HREF,link_rel, ,"Title",ANCHOR_HREF]
    would create a lot of problems.

    
    :return:
    """

    test = "_Hello **World**_"
    expected = [EmphasisText([Text("Hello "),StrongText("World")])]
    actual = TokenizeBody(test)

    assert len(actual) == 1
    assert actual[0].content == expected[0].content