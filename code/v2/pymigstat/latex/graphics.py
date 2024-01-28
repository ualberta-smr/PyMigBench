from latex.core import Node, TagNode


class GraphicsNode(Node):
    def __init__(self, path: str, width: str = None, height: str = None):
        self.path = path
        self.width = width
        self.height = height

    def render(self) -> str:
        opt_args = []
        if self.width:
            opt_args.append("width=" + self.width)
        if self.height:
            opt_args.append("height=" + self.height)

        inner = TagNode("includegraphics", [self.path], opt_args)
        return inner.render()
