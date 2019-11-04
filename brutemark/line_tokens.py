import textwrap

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
    def Render(cls, elements):
        lines = []
        for element in elements:
            lines.append(element.render())

        body = "\n".join(lines)

        product = f"""\
        <generic_line>
            {body}
        </generic_line>"""

        return textwrap.dedent(product)


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
    CAN_NEST = False

    @classmethod
    def Render(cls, elements):
        return "\n" * len(elements)



class TextLine(Line):
    PROCESS_BODY = True
    CAN_NEST = False

    @classmethod
    def TestAndConsume(cls, raw):

        raw, is_nested = test_nested(raw)

        return cls(raw, is_nested)

    @classmethod
    def Render(cls,elements):
        lines = []
        for element in elements:
            line = ""
            if hasattr(element, "render"):
                line = element.render()
            else:
                line = elements

            if line.endswith("  "):
                line += "<br/>"

            lines.append(line)

        body = "\n".join(lines)
        return f"<p>{body}</p>"


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
            lines.append(element.render())

        body = "\n".join(lines)
        return f"<pre><code>{body}</code></pre>"

    def render(self):
        return self.content



class OrderedItemLine(Line):
    REGEX = regexs.ORDERED_ITEM
    PROCESS_BODY = True
    CAN_NEST = True

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
    def Render(cls, elements):
        assert len(elements) == 1

        return elements[0].render()

    def render(self):
        components = []
        if isinstance(self.content, str):
            components.append(self.content)
        else:
            for element in self.content:
                if hasattr(element, "render"):
                    components.append(element.render())
                else:
                    components.append(element)

        body = " ".join(components)

        return f"<h{self.level}>{body}</h{self.level}>"


