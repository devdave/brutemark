r"""

"""

import re
from enum import Enum, auto

from collections import namedtuple

from . import regexs
from . import line_tokens
from .line_tokens import CodeLine, UnorderedItemLine, OrderedItemLine, QuotedLine, HeaderLine, BlankLine, TextLine
from .body_tokens import Token, RawText, Text, EmphasisText, StrongText, Anchor, Image

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
Line based tokens
=================
"""







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
        EmphasisText,
        StrongText,
        Anchor,
        Image
    ]
    product = []

    for processor in processors:

        _, token = processor.Consume(raw)

        if token is not None:
            pre = post = None

            if token.start != 0:
                product.extend(TokenizeBody(raw[:token.start]))

            token.content = TokenizeBody(token.content)
            product.append(token)

            if token.stop != len(raw):
                product.extend(TokenizeBody(raw[token.stop:]))

            break

    else:
        product.append(Text(raw, 0, len(raw)))


    return product

def TokenizeLine(raw:str)->Token:
    """
    :param raw_str:
    :return:
    """
    is_nested = False

    if raw.strip() == "":
        return BlankLine(raw, False)

    processors = [
        line_tokens.HTMLLine,
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
            break

    else:
        return TextLine.TestAndConsume(raw)


