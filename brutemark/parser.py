r"""

"""

import re
from enum import Enum, auto

from collections import namedtuple

from . import regexs
from . import line_tokens
from . import body_tokens
# from .line_tokens import CodeLine, UnorderedItemLine, OrderedItemLine, QuotedLine, HeaderLine, BlankLine, TextLine
# from .body_tokens import Token, RawText, Text, EmphasisText, StrongText, Anchor, Image

def Blocker(raw_text):
    blocks = []
    raw_lines = raw_text.split("\n")

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




class BodyTokenizer():
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
    def __init__(self):
        self.processors = [
            body_tokens.EmphasisText,
            body_tokens.StrongText,
            body_tokens.Anchor,
            body_tokens.Image
        ]
        self.default_processor = [body_tokens.Text]


    def process(self, raw:str)->[]:
        product = []
        for processor in self.processors:

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
            product.append(body_tokens.Text(raw, 0, len(raw)))

        return product

body_tokenizer = BodyTokenizer()
TokenizeBody = body_tokenizer.process

class LineTokenizer(object):

    def __init__(self):
        self.processors = [
            line_tokens.HTMLLine,
            line_tokens.CodeLine,
            line_tokens.QuotedLine,
            line_tokens.UnorderedItemLine,
            line_tokens.OrderedItemLine,
            line_tokens.HeaderLine
        ]

    def process(self, raw:str, last_token:line_tokens.Line = None, stack=None)->line_tokens.Line:

        is_nested = False
        stack = [] if stack is None else stack

        current_processors = last_token.PROCESSORS if last_token is not None else self.processors


        if raw.strip() == "":
            return line_tokens.BlankLine(raw, False)


        for processor in current_processors:
            _, product = processor.TestAndConsume(raw)

            if product is not None:
                return product
                break

        else:
            return line_tokens.TextLine.TestAndConsume(raw)


line_tokenizer = LineTokenizer()
TokenizeLine = line_tokenizer.process