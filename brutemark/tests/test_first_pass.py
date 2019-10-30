from brutemark.parser import Blocker, TokenizeLine, Line

test = """
# Hello World
    This is a code line
    This is a nested code line #2
> This is a block quote
## Second hello world in h2
* Unordered item 1
      This is a nested code line
* Unordered item 2
321. Ordered item 1
* Unordered item 3
1. Ordered Item 2
"""


def test_assure_blocker_works():

    blocks = Blocker(test)
    assert len(blocks) == 1
    lines = blocks[0]
    assert len(lines) == 11


def test_feeding_lines_to_tokenizeline_does_not_break():

    tokenized_blocks = []

    for raw_blocks in Blocker(test):
        tokenized_line = []
        for raw_line in raw_blocks:

            token = TokenizeLine(raw_line)
            assert isinstance(token, Line)

            tokenized_line.append(token)

        tokenized_blocks.append(tokenized_line)


    assert len(tokenized_blocks) == 1
    assert len(tokenized_blocks[0]) == 11


