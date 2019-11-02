import re

"""
# Line based token containers 
As denoted by `^` in the regex

"""
BLANK = re.compile(r"^$")

HTML_LINE = re.compile(
                    r"""^(?!\t) #Ignore if line starts with tab or more than 3 spaces
                        (?!\s{4,})  #TODO I don't feel like fixing right now but this fails to match if there are ANY spaces
                            (?P<content>\<[^\>]+\>) #Match <ANYTHING> that is wrapped with greater/less than symbols
                    """, re.VERBOSE)

CODE_LINE = re.compile(r"(^\ {4})|(^\t)")
START_WS = re.compile(r"^(\s+)")
QUOTED = re.compile(r"^(\>)")

ORDERED_ITEM = re.compile(r"^\d{1,}\.") # (Numeric)(period)
UNORDERED_ITEM = re.compile(r"^\* ")

LINE_HEADER = re.compile(r"""^(?P<content>\#+)\ """)

"""
    Body tokens
"""

ANCHOR_simple = re.compile(r"""\[
                                (?P<content>[^\]]+)
                                \]
                                \(
                                (?P<href>[^\)]+)
                                \)""", re.VERBOSE)

ANCHOR_title =  re.compile(r"""\[
                                (?P<content>[^\]]+)
                                \]
                                \(
                                (?P<href>[^\)]+)
                                 \"(?P<title>[^\"]+)\"
                                \)""", re.VERBOSE)

IMAGE_simple = re.compile(r"""\!\[(?P<content>[^\]]+)\]\((?P<href>[^\)]+)\)""")
IMAGE_title =  re.compile(r"""\!\[(?P<content>[^\]]+)\]\((?P<href>[^\)]+) \"(?P<title>[^\"]+)\"\)""")



STRONG_underscore = re.compile(r"""(\_{2}(?P<content>[^_]+)\_{2})""")
STRONG_star = re.compile(
                        r"""(
                        (?<!\\)
                        \*{2}
                        (?P<content>[^_]+)
                        (?<!\\)
                        \*{2}
                        )""", re.VERBOSE)

EMPHASIS_underscore = re.compile(
                            r"""(
                            (?<!\_) #if there is double __ at the start, ignore
                            \_
                            (?P<content>[^\_]+)
                            \_                            
                            (?!\_) #if there is double __ at the end, ignore
                            )""", re.VERBOSE)
EMPHASIS_star = re.compile(
                            r"""
                            (?<!\\)
                            (?<!\*)
                            \*
                            (?P<content>[^\*]+)
                            (?<!\\)
                            \*
                            (?!\*)
                            """, re.VERBOSE)


