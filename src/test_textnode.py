import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_link_should_fail(self):
        # test link withou url should fail
        try:
            TextNode("This is a text node", TextType.LINK, None)
        except ValueError as e:
            self.assertEqual(e.args[0], "url must be provided")

    def test_image_should_fail(self):
        # test link withou url should fail
        with self.assertRaises(ValueError) as e:
            TextNode("This is a text node", TextType.IMAGE, None)
        self.assertEqual(str(e.exception), "url must be provided")

    def test_text_without_text_should_fail(self):
        with self.assertRaises(ValueError)as e:
            TextNode("", TextType.TEXT)
        self.assertEqual(str(e.exception), "text should not be empty")


class TestTextType(unittest.TestCase):
    def test_text_type(self):
        self.assertEqual(TextType.TEXT.value, "text")
        self.assertEqual(TextType.BOLD.value, "bold")
        self.assertEqual(TextType.ITALIC.value, "italic")
        self.assertEqual(TextType.CODE.value, "code")
        self.assertEqual(TextType.LINK.value, "link")
        self.assertEqual(TextType.IMAGE.value, "image")


class TestTextToHtmlFunction(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, {})

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Hello, world!", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, {})

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("Hello, world!", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, {})

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("Hello, world!", TextType.CODE)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, {})

    def test_text_node_to_html_node_link(self):
        text_node = TextNode(
            "Hello, world!", TextType.LINK, "http://test.com")
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props["href"], "http://test.com")

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("My Image", TextType.IMAGE, "my_image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "my_image.png")
        self.assertEqual(html_node.props["alt"], "My Image")

    def test_text_node_to_html_node_invalid(self):

        text_node = TextNode("Hello, world!", "unhandled_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()
