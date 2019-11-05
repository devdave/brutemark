from brutemark.parser import Blocker
test = \
"""This is paragraph one it is all on one line and then given two empty lines


this is paragraph two it 
is broken into individual
blocks with no spaces between them


This 
is 
paragraph 
three 
, 
it 
is 
kind 
of 
nonsensical 
because 
the 
whole 
thing 
is 
one 
word 
followed 
by 
a 
space 
and 
then 
a 
carriage 
return.
"""


def test_total_block_count_is_three():
    blocks = Blocker(test)
    assert len(blocks) == 3


def test_block_sizes_are_correct():
    blocks = Blocker(test)
    assert len(blocks[0]) == 1
    assert len(blocks[1]) == 3
    assert len(blocks[2]) == 27