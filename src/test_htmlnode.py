import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_NotImplemented_should_fail(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_should_succeed(self):
        node = HTMLNode("p", "test text", [], {"hello": "world"})
        self.assertEqual(node.__repr__(),
                         "HTMLNode(p, test text, [], {'hello': 'world'})"
                         )

    def test_empty_props_should_succeed(self):
        node = HTMLNode().props_to_html()
        self.assertEqual(node, "")

    def test_props_should_succeed(self):
        node = HTMLNode(props={
            "src": "images/cat.png",
            "alt": "A cute cat",
            "width": "500"
        }

        ).props_to_html()
        self.assertEqual(
            node, ' src="images/cat.png" alt="A cute cat" width="500"')

    def test_multiple_props_should_succeed(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank"
            }
        ).props_to_html()
        self.assertEqual(
            node, ' href="https://www.google.com" target="_blank"')


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_without_props(self):
        node = LeafNode("p", "This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_leaf_node_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://example.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://example.com">Click me!</a>')

    def test_leaf_node_without_tag(self):
        node = LeafNode(None, "Just text.")
        self.assertEqual(node.to_html(), "Just text.")

    def test_leaf_node_without_value(self):
        with self.assertRaises(ValueError) as er:
            LeafNode("div", None)
        self.assertEqual(str(er.exception), "value required")


class TestParentNode(unittest.TestCase):
    def test_parent_node_with_div(self):
        parent = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text")
            ]
        )
        self.assertEqual(parent.to_html(),
                         "<div><b>Bold text</b>Normal text</div>")

    def test_nested_parent(self):

        nested_parent = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "Nested text")
                    ]
                )
            ]
        )
        self.assertEqual(nested_parent.to_html(),
                         "<div><p>Nested text</p></div>")

    def test_prop_handling(self):
        parent = ParentNode(
            "div",
            [
                LeafNode(None, "Text")
            ],
            props={"class": "test-class"}
        )
        self.assertEqual(
            parent.to_html(),
            '<div class="test-class">Text</div>'
        )

    def test_deeper_nesting(self):
        layered = ParentNode(
            "section",
            [
                ParentNode(
                    "article",
                    [
                        LeafNode("h1", "Welcome")
                    ]
                )
            ]
        )
        self.assertEqual(
            layered.to_html(),
            "<section><article><h1>Welcome</h1></article></section>"
        )

    def test_parent_tag_error(self):
        with self.assertRaises(ValueError) as er:
            ParentNode("div", None)
        self.assertEqual(str(er.exception), "children required")
        pass

    def test_children_error(self):
        with self.assertRaises(ValueError) as er:
            ParentNode(None,
                       [
                           LeafNode(None, "Text")
                       ],
                       )
        self.assertEqual(str(er.exception), "tag required")


if __name__ == "__main__":
    unittest.main()
