r"""

"""

import re
from enum import Enum, auto

from collections import namedtuple

def Blocker(raw_text):
    blocks = []
    raw_lines = raw_text.strip().split("\n")

    buffer = []
    spaces = 0
    while len(raw_lines):
        line = raw_lines.pop(0)
        buffer.append(line)

        if line == "":
            spaces += 1
        else:
            spaces = 0

        if spaces >= 2:
            if buffer:
                if buffer[-2] == "" and buffer[-1] == "":
                    blocks.append(buffer[:-2])
                else:
                    blocks.append(buffer)

            buffer = []
            spaces = 0

    if buffer:
        blocks.append(buffer)

    return blocks


"""
    
Inline/embedded Tokens
======================
    emphasis em
    strong strong
    strikethrough del
    anchor
    image
    
"""

class Token(object):

    REGEX = None

    def __init__(self, content):
        self.content = content

    @classmethod
    def Consume(cls, raw):
        """
            Consume is complicated versus Line tokens
            because it expects to start with str and convert that to
                pre:str, token, post:str
            on success OR
                pre:str, None, None
            on a miss
        """
        assert cls.REGEX is not None, f"{cls!r} expected to have REGEX attribute not None for {raw!r}"

        product = None
        post = None

        regexs = [cls.REGEX]if isinstance(cls.REGEX, list) is False else cls.REGEX

        for regex in regexs:
            match = regex.search(raw)

            if match is not None:

                match_start = match.start(0)-1
                match_end = match.end(0)+1

                post = None if len(raw) == match_end else raw[match_end:]
                product = cls(match.group(1))
                raw = None if match_start == 0 else raw[:match_start]
                return raw, product, post

        else:
            return raw, None, None

class RawText(Token):

    @classmethod
    def Consume(cls, raw):
        return cls(raw)

class Text(Token):
    REGEX = re.compile(r"(.+)")


class EmphasisText(Text):
    REGEX = [Regexs.EMPHASIS_underscore, Regexs.EMPHASIS_star]
    pass

class StrongText(Text):
    REGEX = [Regexs.STRONG_star, Regexs.STRONG_underscore]
    pass

class Anchor(Token):
    REGEX = Regexs.ANCHOR
    pass

class Image(Token):
    REGEX = Regexs.IMAGE
    pass

"""    
Line based tokens
=================
"""

def test_nested(raw):
    match = Regexs.START_WS.match(raw)

    if match is not None:
        raw = raw[match.end():]

    return raw, match is not None

class Line(object):
    REGEX = None
    BODY_PROCESSOR = RawText

    def __init__(self, content, nested=False):
        self.content = content
        self.nested = nested

    @classmethod
    def TestAndConsume(cls, raw):
        assert cls.REGEX is not None, f"Expected {cls} to have a REGEX assigned"
        product = None
        raw, is_nested = test_nested(raw)

        match = cls.REGEX.match(raw)
        if match is not None:
            product = cls(raw[match.end():], is_nested)

        return raw, product


class BlankLine(Line):
    pass

class TextLine(Line):
    @classmethod
    def TestAndConsume(cls, raw):

        raw, is_nested = test_nested(raw)

        return cls(raw, is_nested)


class QuotedLine(Line):
    REGEX = Regexs.QUOTED
    pass


class CodeLine(Line):
    REGEX = Regexs.CODELINE

    @classmethod
    def TestAndConsume(cls, raw):
        assert cls.REGEX is not None, f"Expected {cls} to have a REGEX assigned"
        product = None
        match = cls.REGEX.match(raw)

        if match is not None:
            raw, is_nested = test_nested(raw[match.end():])
            product = cls(raw, is_nested)

        return raw, product


class OrderedItemLine(Line):
    REGEX = Regexs.ORDERED_ITEM
    pass

class UnorderedItemLine(Line):
    REGEX = Regexs.UNORDERED_ITEM
    pass

class HeaderLine(Line):

    REGEX = Regexs.LINE_HEADER

    def __init__(self, raw, is_nested=False, level=1):
        self.level= level
        super().__init__(raw, is_nested)



    @classmethod
    def TestAndConsume(cls, raw):
        product = None
        raw, is_nested = test_nested(raw)

        match = cls.REGEX.match(raw)

        if match is not None:
            level = match.string.strip().count("#")
            product = cls(raw[:match.end()], is_nested, level)

        return raw, product



def TokenizeBody(raw:str)->[]:
    """
        given a string like
            hello __world__ this *is* a **test** of [Markdown](https://daringfireball.net/projects/markdown/ "Markdown homepage")
        creates
            [
                Text("Hello "),
                Emphasis(Text("world")),
                Text(" this "),
                Emphasis(Text("is")),
                Text(" a "),
                Strong(Text("test"),
                Text(" of "),
                Anchor(body=Text("Markdown",href="https://daringfireball.net/projects/markdown/", title="Markdown homepage")
            ]

    :param raw:str
    :return:
    """
    processors = [
        StrongText,
        EmphasisText,
        Anchor,
        Image
    ]
    processed_line = []


    for processor in processors:

        pre, token, post = processor.Consume(raw)

        if token is not None:
            if pre is not None and pre != "":
                processed_line.extend(TokenizeBody(pre))

            processed_line.append(token)

            if post is not None and post != "":
                processed_line.extend(TokenizeBody(post))

            return processed_line

    return [Text(raw)]

def TokenizeLine(raw:str)->Token:
    """
    :param raw_str:
    :return:
    """
    is_nested = False

    if raw.strip() == "":
        return BlankLine(raw, False)

    # raw, codeline = CodeLine.TestAndConsume(raw)
    #
    # if codeline is not None:
    #     return codeline

    processors = [
        CodeLine,
        QuotedLine,
        UnorderedItemLine,
        OrderedItemLine,
        HeaderLine
    ]

    for processor in processors:
        _, product = processor.TestAndConsume(raw)

        if product is not None:
            return product

    else:
        return TextLine.TestAndConsume(raw)


