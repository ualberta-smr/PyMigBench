from abc import abstractmethod, ABC


class Node(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class TextNode(Node):
    def __init__(self, text):
        self.text = text

    def render(self):
        return self.text

    def __str__(self):
        return self.text


class TagNode(Node):
    _content: str

    def __init__(self, tag_name: str, mandatory_args: list[any] = None,
                 optional_args: list[any] = None):
        self.tag_name = tag_name
        self.mandatory_args = mandatory_args or []
        self.optional_args = optional_args or []
        self._build()

    def render(self):
        return self._content

    def __str__(self):
        return self._content

    def _build(self):
        self._content = "\\" + self.tag_name + TagNode.build_args(self.mandatory_args, self.optional_args)

    @staticmethod
    def build_args(mandatory_args: list[str], optional_args: list[str]):
        args = ""
        if optional_args:
            args += "[" + (", ".join(str(arg) for arg in optional_args)) + "]"
        if mandatory_args:
            args += "".join("{" + str(arg) + "}" for arg in mandatory_args)

        return args


class GroupNode(Node):
    _children: list[Node]

    def __init__(self):
        self._children = []

    def add_child(self, child: Node):
        self._children.append(child)
        return self

    def add_text(self, text: str):
        return self.add_child(TextNode(text))

    def add_tag(self, tag: str, *args):
        return self.add_child(TagNode(tag, [*args]))

    def start_line(self, indentation=0):
        self._children.append(TextNode("\n"))
        self._children.append(TextNode(" " * (2 * indentation)))
        return self

    def render(self):
        return "".join(c.render() for c in self._children)


class BeginEndNode(GroupNode):
    _add_auto_generation_warning: bool = False

    def __init__(self, indentation=0, name: any = None, mandatory_args: list[str] = None,
                 optional_args: list[str] = None):
        super().__init__()
        self.indentation = indentation
        self.name = name
        self.mandatory_args = mandatory_args or []
        self.optional_args = optional_args

    def add_warning(self):
        self._add_auto_generation_warning = True
        return self

    def render(self):
        final = GroupNode()
        if self._add_auto_generation_warning:
            final.add_text("% WARNING: This content in auto generated. Any manual edits will be lost on regeneration.")

        final.start_line(self.indentation).add_child(TagNode("begin", [self.name]))
        final.add_text(TagNode.build_args(self.mandatory_args, self.optional_args))

        for child in self._children:
            final.add_child(child)
        final.start_line(self.indentation).add_child(TagNode("end", [self.name]))
        return final.render()
