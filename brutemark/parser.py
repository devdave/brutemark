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


class Regexs:

    BLANK = re.compile(r"^$")

    CODELINE = re.compile(r"(^\ {4})|(^\t)")
    START_WS = re.compile(r"^(\s+)")
    QUOTED = re.compile(r"^(\>)")

    ORDERED_ITEM = re.compile(r"^\d{1,}\.") # (Numeric)(period)
    UNORDERED_ITEM = re.compile(r"^\* ")

    ANCHOR = re.compile(r"""\[([^\]]+)\]\(([^\)]+)\)|\[([^\]]+)\]\(([^\)]+)( "[^"]")\)""")
    IMAGE = re.compile(r"""\!\[([^\]]+)\]\(([^\)]+)\)|\!\[([^\]]+)\]\(([^\)]+)( "[^"]")\)""")

    STRONG_underscore = re.compile(r"""(\_{2}([^_]+)\_{2})""")
    STRONG_star = re.compile(r"""(\*{2}([^_]+)\*{2})""")
    EMPHASIS_underscore = re.compile(r"\_([^\_]+)\_")
    EMPHASIS_star = re.compile(r"(\*{2}([^\*]+)\*{2})")


    LINE_HEADER = re.compile(r"""^((\#+) )""")


Token = namedtuple("Token", "content,type,nested")

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
def test_nested(raw):
    match = Regexs.START_WS.match(raw)

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


    # raw, quoted_line = QuotedLine.TestAndConsume(raw)
    #
    # if quoted_line is not None:
    #     return quoted_line
    #
    # raw, unordered_line = UnorderedItemLine.TestAndConsume(raw)
    #
    # if unordered_line is not None:
    #     return unordered_line
    #
    #
    #
    # # if Regexs.QUOTED.match(raw):
    # #     match = Regexs.QUOTED.match(raw)
    # #     raw = raw[match.end():]
    # #
    # #     return QuotedLine(TokenizeBody(raw), is_nested)
    #
    # elif Regexs.UNORDERED_ITEM.match(raw):
    #     match = Regexs.UNORDERED_ITEM.match(raw)
    #     raw = raw[match.end():]
    #     return UnorderedItemLine(TokenizeBody(raw), is_nested)
    #
    # elif Regexs.ORDERED_ITEM.match(raw):
    #     match = Regexs.ORDERED_ITEM.match(raw)
    #     raw = raw[match.end():]
    #     return OrderedItemLine(TokenizeBody(raw), is_nested)
    #
    #
    # else:
    #     return TextLine(TokenizeBody(raw), is_nested)






















# class TextToken(object):
#
#     def __init__(self, raw_str):
#         self.body = raw_str
#
#
#
# class BaseTokenizedLine(object):
#     __slots__ = ("tokens", "nested")
#
#     def __init__(self, nested = False):
#         self.tokens = []
#         self.nested = nested
#
#         if raw_line is not None:
#             self.tokens.append(TextToken(raw_line))
#
#
#
#
# class CodeLine(BaseTokenizedLine):
#
#     def __init__(self, raw_line):
#         super(self).__init__(raw_line)
#
# class QuotedLine(BaseTokenizedLine):
#     def __init__(self, raw_line):
#         super(self).__init__(raw_line)




# class TokenTypes(Enum):
#     BLANK = 1
#     HEADER = 2 # first line token starts with at least one #
#
#     CODE_MARK = 3 #Is ``` by itself
#
#     CODE_SPACE = 4 #Is four spaces
#     CODE_TAB = 4
#     CODE_LINE_START = 4
#
#     BLOCKQUOTE = 5
#
#     LINE_ITEM_UNORDERED =  6    # *
#     LINE_ITEM_ORDERED = 7       # \d{1,}\.
#     TABLE_CELL = 8              # starts with |
#     TEXT = 9                    # Whatever didn't match above
#

#
#
#
# class Token(object):
#     __slots__ = ("type", "content")
#
#     def __init__(self, type=):
#         self.content = []
#
#
# class TokenLine(object):
#     __slots__ = ("type", "tokens", "nested")
#
#     def __init__(self, type = TokenTypes.TEXT, nested=False):
#         self.type = type
#         self.nested = nested
#         self.tokens = []
#
#     def append(self, token):
#         self.tokens.append(token)
#
#     def __iter__(self):
#         for token in self.tokens:
#             yield token
#
# class TextLine(object):
#     def __init__(self, nested=False):
#         self.type = TokenTypes.TEXT
#         if
#
# class CodeLine(TokenLine):
#     """
#         Anything after Code start is considered TextToken.
#
#         TODO: allow for nested code blocks like
#
#         <li>
#             <p>Hello World</p>
#             <code>
#                 x = 123
#                 y = x - 20
#                 x == 103
#             </code>
#         </li>
#     """
#
#
#     def __init__(self, raw_line):
#
#
#
#
#
# def BlockTokenizer(block:list):
#
#     for line in block: # type: str
#         current_line = TokenLine()
#
#         if line.strip() == "":
#             current_line.type = TokenTypes.BLANK
#             continue
#
#         # Check for code block escapes
#         if line.startswith("\t"):
#             current_line.type = TokenTypes.CODE_LINE_START
#             line = line[1:]
#         elif Regexs.STARTING_FOUR_SPACE.match(line) is not None:
#             match = Regexs.STARTING_FOUR_SPACE.match(line)
#             current_line.type = TokenTypes.CODE_LINE_START
#             line = line[match.pos:match.endpos]
#
#         if current_line.type == TokenTypes.CODE_LINE_START:
#             token = Token()
#
#         #look for spaces and tabs in excess of code block starts
#         if Regexs.START_WS.match(line) is not None:
#             match = Regexs.START_WS.match(line)
#             current_line.nested = True
#             line = line[match.pos, tch.endpos]
#
#         if current_line.type == TokenTypes.CODE_LINE_START:
#             token = Token(TokenTypes.TEXT)
#             token.append(line)
#             continue
#
#         if line[0] == ">":
#             current_line.type = TokenTypes.BLOCKQUOTE
#             line = line[1:]
#         elif line[0:1] == "* ":
#             current_line.type = TokenTypes.LINE_ITEM_UNORDERED
#             line = line[2:]
#         elif Regexs.ORDERED_RE.match(line):
#             match = Regexs.ORDERED_RE.match(line)
#             current_line.type = TokenTypes.LINE_ITEM_ORDERED
#             line = line[match.pos, ma]
#
#
#
#
#         for fragment in line.split(ParserBasics.TOKEN_SEP):
#
#
#         yield ParserBasics.NEWLINE
#
#     else:
#
#
#
#
#
#

#
#
#
#