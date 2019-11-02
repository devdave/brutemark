
from . import regexs

def test_nested(raw):
    match = regexs.START_WS.match(raw)

    if match is not None:
        raw = raw[match.end():]

    return raw, match is not None


class Line(object):
    REGEX = None

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
    REGEX = regexs.QUOTED
    pass

class HTMLLine(Line):
    REGEX = regexs.HTML_LINE

    @classmethod
    def TestAndConsume(cls, raw):
        product = None
        match = cls.REGEX.match(raw)
        is_nested = False

        if match is not None:
            product = cls(raw, is_nested)

        return raw, product



class CodeLine(Line):
    REGEX = regexs.CODE_LINE

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
    REGEX = regexs.ORDERED_ITEM
    pass

class UnorderedItemLine(Line):
    REGEX = regexs.UNORDERED_ITEM
    pass

class HeaderLine(Line):

    REGEX = regexs.LINE_HEADER

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