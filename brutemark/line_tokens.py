import textwrap

from lxml.html.builder import E
from lxml.html import fromstring

from . import regexs
from . import body_tokens

def test_nested(raw):
    match = regexs.START_WS.match(raw)

    if match is not None:
        raw = raw[match.end():]

    return raw, match is not None


class Line(object):
    REGEX = None
    PROCESS_BODY = False
    CAN_NEST = False
    ALLOWED_NESTED = []
    CAN_CONTAIN = [body_tokens.Text]

    def __init__(self, content, nested=False):
        self.content = content
        self.nested = nested

    @classmethod
    def Contains(cls, new_line):
        return type(new_line) == cls

    @classmethod
    def Render(cls, elements):
        lines = []
        for element in elements:
            lines.append(element.render())

        body = "\n".join(lines)

        element = E(cls.__name__)
        element.text = body

        return element


    def render(self):
        line = []
        for element in self.content:
            if hasattr(element, "render"):
                line.append(element.render())
            else:
                line.append(element)

        return " ".join(line)


    @classmethod
    def TestAndConsume(cls, raw):
        assert cls.REGEX is not None, f"Expected {cls} to have a REGEX assigned"
        product = None
        raw, is_nested = test_nested(raw)

        match = cls.REGEX.match(raw)
        if match is not None:
            product = cls(match.group("content"), is_nested)

        return raw, product


class BlankLine(Line):


    @classmethod
    def Render(cls, elements):
        #No matter how many blanklines, just do one <br/>
        return E("br")



class TextLine(Line):
    PROCESS_BODY = True


    @classmethod
    def Contains(cls, new_token):
        return type(new_token) == cls

    def can_nest(self, new_line):
        """
            Paragraph/text lines can be merged together
        """
        return type(new_line) == TextLine

    @classmethod
    def TestAndConsume(cls, raw):

        raw, is_nested = test_nested(raw)

        return cls(raw, is_nested)

    @classmethod
    def Render(cls, children):

        lines = []
        for child_token in children:
            child_token.render(lines)

        paragraph = E("p", *lines)
        return paragraph

    def render(self, container:list):
        for body_token in self.content:
            container.append(body_token.render())

        if hasattr(container[-1], "endswith"):
            if container[-1].endswith("  "):
                container.append(E("br"))

        return container



class QuotedLine(Line):
    REGEX = regexs.QUOTED
    PROCESS_BODY = True
    CAN_NEST = False

class HTMLLine(Line):
    REGEX = regexs.HTML_LINE
    CAN_NEST = False
    # PROCESS_BODY is defaulted to False

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
    CAN_CONTAIN = [None, body_tokens.RawText, body_tokens.Text]
    # PROCESS_BODY is defaulted to False

    @classmethod
    def TestAndConsume(cls, raw):
        assert cls.REGEX is not None, f"Expected {cls} to have a REGEX assigned"
        product = None
        match = cls.REGEX.match(raw)

        if match is not None:
            raw, is_nested = test_nested(raw[match.end():])
            product = cls(raw, is_nested)

        return raw, product

    @classmethod
    def Render(cls, elements):
        lines = []
        for element in elements:
            # Codeline does not have preprocessed bodies
            lines.append(element.content)

        body = "\n".join(lines)
        return E("pre", E("code", body))





class OrderedItemLine(Line):
    REGEX = regexs.ORDERED_ITEM
    PROCESS_BODY = True
    CAN_NEST = True

    @classmethod
    def Render(cls, elements):
        lines = []
        for token in elements:
            if hasattr(token, "render"):
                lines.append(token.render())
            else:
                lines.append(E("li", token.content))

        return E("ol", *lines)

    def render(self):
        pieces = []
        for element in self.content:
            if hasattr(element, "render"):
                pieces.append(element.render())
            else:
                pieces.append(element)

        return E("li", *pieces)


class UnorderedItemLine(Line):
    REGEX = regexs.UNORDERED_ITEM
    PROCESS_BODY = True
    CAN_NEST = True

class HeaderLine(Line):

    REGEX = regexs.LINE_HEADER
    PROCESS_BODY = True
    CAN_NEST = False



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
            product = cls(match.group("content"), is_nested, level)

        return raw, product

    @classmethod
    def Render(cls, elements=None):
        assert len(elements) == 1
        sub_elements = [x.render() for x in elements[0].content]
        header = E(f"h{elements[0].level}", *sub_elements)
        return header

    def render(self):
        raise NotImplementedError("HeaderLine is rendered through classmethod Render")


