import re

from . import regexs


class Token(object):

    __slots__ = ("content", "start", "stop", "attrs")

    REGEX = None
    CONTENT_RULES = []

    def __init__(self, content, start, stop, **attrs):
        self.content = content
        self.start = start
        self.stop = stop
        self.attrs = attrs

    def __repr__(self): # pragma: no cover
        return f"<{self.__class__.__name__} content={self.content!r}>"



    def contains_token(self, other_token):
        return other_token.stop <= self.stop and other_token.start >= self.start


    def render(self):
        product = []

        if isinstance(self.content, str):
            product.append(self.content)
        else:
            for element in self.content:
                if hasattr(element, "render"):
                    product.append(element.render())
                else:
                    product.append(element)

        return " ".join(product)

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
        # assert len(cls.CONTENT_RULES) != 0, f"{cls!r} must have CONTENT_RULES set"

        product = None
        post = None

        regexs = [cls.REGEX]if isinstance(cls.REGEX, list) is False else cls.REGEX

        for regex in regexs:
            match = regex.search(raw)

            if match is not None:

                match_start = match.start()
                match_end = match.end()
                product = cls(match.group("content"), match_start, match_end)
                return raw, product
        else:
            return raw, None

class RawText(Token):

    @classmethod
    def Consume(cls, raw):
        return cls(raw)

class Text(Token):
    REGEX = re.compile(r"(.+)")

    @classmethod
    def Render(cls, token):
        return token.content


class EmphasisText(Token):
    REGEX = [regexs.EMPHASIS_underscore, regexs.EMPHASIS_star]


class StrongText(Token):
    REGEX = [regexs.STRONG_star, regexs.STRONG_underscore]


class Anchor(Token):
    REGEX = [regexs.ANCHOR_title, regexs.ANCHOR_simple]

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
        # assert len(cls.CONTENT_RULES) != 0, f"{cls!r} must have CONTENT_RULES set"

        product = None
        post = None

        regexs = [cls.REGEX]if isinstance(cls.REGEX, list) is False else cls.REGEX

        for regex in regexs:
            match = regex.search(raw)

            if match is not None:

                match_start = match.start(0)
                match_end = match.end(0)+1
                groups = match.groupdict()
                if "content" in groups:
                    del groups['content']

                product = cls(match.group(1), match_start, match_end, **groups)
                return raw, product
        else:
            return raw, None


class Image(Token):
    REGEX = [regexs.IMAGE_title, regexs.IMAGE_simple]
