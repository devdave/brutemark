import re

"""
# Line based token containers 
As denoted by `^` in the regex

"""
BLANK = re.compile(r"^$")

CODELINE = re.compile(r"(^\ {4})|(^\t)")
START_WS = re.compile(r"^(\s+)")
QUOTED = re.compile(r"^(\>)")

ORDERED_ITEM = re.compile(r"^\d{1,}\.") # (Numeric)(period)
UNORDERED_ITEM = re.compile(r"^\* ")

"""
    Body tokens
"""

ANCHOR_simple = re.compile(r"""\[
                                (?P<content>[^\]]+)
                                \]
                                \(
                                (?P<href>[^\)]+)
                                \)""", re.VERBOSE)

STRONG_underscore = re.compile(r"""(\_{2}([^_]+)\_{2})""")
STRONG_star = re.compile(r"""(\*{2}([^_]+)\*{2})""")
EMPHASIS_underscore = re.compile(r"\_([^\_]+)\_")
EMPHASIS_star = re.compile(r"(\*{2}([^\*]+)\*{2})")
ANCHOR_title =  re.compile(r"""\[
                                (?P<content>[^\]]+)
                                \]
                                \(
                                (?P<href>[^\)]+)
                                 \"(?P<title>[^\"]+)\"
                                \)""", re.VERBOSE)

IMAGE_simple = re.compile(r"""\!\[(?P<content>[^\]]+)\]\((?P<href>[^\)]+)\)""")
IMAGE_title =  re.compile(r"""\!\[(?P<content>[^\]]+)\]\((?P<href>[^\)]+) \"(?P<title>[^\"]+)\"\)""")

LINE_HEADER = re.compile(r"""^((\#+) )""")