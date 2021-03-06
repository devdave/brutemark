from lxml.html.builder import E
from lxml.html import tostring

from collections import defaultdict

from .parser import TokenizeLine, TokenizeBody, Blocker


class ROOT_CONTAINER:

    def __init__(self):
        self.content = None


    @classmethod
    def Contains(cls, child):
        return True

    @classmethod
    def Render(cls, elements):
        grouped = defaultdict(list)

        for element in elements:
            if hasattr(element, "render"):
                pass


    def render(self, content, children):

        leafs = []
        for child in children:
            if hasattr(child, "render"):
                leafs.append(child.render)
            else:
                leafs.append(child)

        return E("div", **leafs)




class Tree:

    def __init__(self, token=None, parent=None, nested=0):
        self.type = type(token)
        self.content = token
        self.nested = nested

        self.parent = parent
        self.children = []



    @classmethod
    def MakeRoot(cls):
        return cls(ROOT_CONTAINER(),parent=None)


    def __repr__(self):
        return f"<{self.__class__.__name__} type={self.type!r}>"

    def add_child(self, child_token):
        branch = Tree(child_token, self, nested=child_token.nested)
        self.children.append(branch)
        return branch

    def add(self, line_token):

        if self.type == ROOT_CONTAINER:
            branch = self.add_child(line_token)
        elif self.type.Contains(line_token) is False:
            branch = self.parent.add(line_token)
        elif self.type.Contains(line_token) is True:
            if line_token.nested > self.nested:
                self.content.content.append(line_token)
                branch = Tree(line_token, self)
            elif line_token.nested < self.nested:
                branch = self.parent.add_child(line_token)
            else:
                self.add_child(line_token)
                branch = self
        else:
            branch = self.add_child(line_token)

        return branch

    def render(self, parent_element = None):

        if self.type == ROOT_CONTAINER:
            kwargs = {"class": "brutemark_root"}
            parent_element = E("div", **kwargs)

            for branch in self.children:
                branch.render(parent_element)
        else:
            branches = [self.content]
            branches.extend([x.content for x in self.children])
            child_element = self.type.Render(branches)
            parent_element.append(child_element)

        return parent_element




def markdown(raw_string, return_tree=False, pretty_print=True):

    tokenized_document = []
    for block in Blocker(raw_string):
        tokenized_block = []
        last_token = None
        for line in block:
            last_token = line_token = TokenizeLine(line, last_token=last_token, stack=tokenized_block)

            if line_token.PROCESS_BODY is True:
                line_token.content = TokenizeBody(line_token.content)

            tokenized_block.append(line_token)
        tokenized_document.append(tokenized_block)
        tokenized_block = []


    #Consolidate lines in a block

    root = Tree.MakeRoot()

    current_branch = root

    for block in tokenized_document:
        for line in block:
            current_branch = current_branch.add(line)

    if return_tree is not False:
        return root
    elif pretty_print is not True:
        return tostring(root.render(), encoding="unicode")
    else:
        return tostring(root.render(), pretty_print=pretty_print, encoding="unicode")




