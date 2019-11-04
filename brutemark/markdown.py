from .parser import TokenizeLine, TokenizeBody, Blocker

ROOT_CONTAINER = "Root"

class Tree:

    def __init__(self, block_type, parent):
        self.type = block_type
        self.parent = parent
        self.children = []
        self.content = []

    def __repr__(self):
        return f"<{self.__class__.__name__} type={self.type!r}>"

    def create_child(self, line):
        branch = Tree(type(line), self)
        self.children.append(branch)
        return branch

    def add(self, line):

        if self.type == ROOT_CONTAINER:
            branch = self.create_child(line)

        elif self.type != type(line):


            if line.nested is True: # TODO check nesting is allowed
                branch = Tree(type(line), self)
                self.children.append(branch)
            else:
                branch = self.parent.create_child(line)

        elif self.type == type(line):
            branch = self
        else:
            raise Exception("To fix")

        branch.content.append(line)


        return branch


    def render(self):
        output = []
        if self.type == ROOT_CONTAINER:
            for element in self.children:
                output.append(element.render())
        else:

            if self.content:
                output.append(self.type.Render(self.content))

            if self.children:
                for child in self.children:
                    output.append(child.render())

        return "\n".join(output)









def markdown(raw_string, return_tree=False):

    tokenized_document = []
    for block in Blocker(raw_string):
        tokenized_block = []
        for line in block:
            tokenized_lined = TokenizeLine(line)
            if tokenized_lined.PROCESS_BODY is True:
                tokenized_lined.content = TokenizeBody(tokenized_lined.content)

            tokenized_block.append(tokenized_lined)
        tokenized_document.append(tokenized_block)
        tokenized_block = []


    #Consolidate lines in a block

    root = Tree(ROOT_CONTAINER, None)

    current_branch = root


    for block in tokenized_document:
        for line in block:
            current_branch = current_branch.add(line)


    return root.render() if return_tree is False else root




