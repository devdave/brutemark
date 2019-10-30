
from brutemark.parser import TokenizeLine, HeaderLine

tests = [
    "# h1",
    "## h2",
    "### h3",
    "#### h4",
    "##### h5",
    "###### h6"
]

nested_tests = [
    "  # h1",
    "  ## h2",
    "  ### h3",
    "  #### h4",
    "  ##### h5",
    "  ###### h6"
]


def test_all_headers():

    for position, test_str in enumerate(tests):
        token = TokenizeLine(test_str)
        assert isinstance(token, HeaderLine)
        assert token.level == position + 1, f"Expected {position+1} for level but got {token.level} with {test_str!r}"
        assert token.nested == False

def test_all_nested_headers():

    for position, test_str in enumerate(nested_tests):
        token = TokenizeLine(test_str)
        assert isinstance(token, HeaderLine)
        assert token.level == position + 1, f"Expected {position+1} for level but got {token.level} with {test_str!r}"
        assert token.nested == True