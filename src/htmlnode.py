class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        html_props = " "
        for key, value in self.props.items():
            html_props += f'{key}="{value}" '
        return html_props.rstrip()

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None,  props=None):
        if props is None:
            props = {}
        if not value and tag != "img":
            raise ValueError("value required")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("value required")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if not tag:
            raise ValueError("tag required")
        if not children:
            raise ValueError("children required")
        super().__init__(tag, None, children, props)

    def to_html(self):
        child_list = []
        if not self.tag:
            raise ValueError("tag required")
        if not self.children:
            raise ValueError("children required")
        for child in self.children:
            child_list.append(child.to_html())
        text = "".join(child_list)
        return f"<{self.tag}{self.props_to_html()}>{text}</{self.tag}>"
