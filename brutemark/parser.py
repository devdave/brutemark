r"""

"""

import re
from enum import Enum, auto

from collections import namedtuple

from . import regexs
from .line_tokens import CodeLine, UnorderedItemLine, OrderedItemLine, QuotedLine, HeaderLine, BlankLine

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


