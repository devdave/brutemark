from lxml.html.builder import E
from lxml.html import tostring, fromstring
from brutemark.markdown import markdown

def test_inline_HTML():

    test = \
"""<table>
  <tr>
   <td>Foo</td>
  </tr>
</table>"""

    root = E("div", **{"class":"markdown_root"})

    expected = \
"""<div class="brutemark_root"><table>
  <tr>
   <td>Foo</td>
  </tr>
</table></div>"""


    actual = markdown(test, pretty_print=False)
    assert actual == expected