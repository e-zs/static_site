#python

import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is another text node', TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_text_type(self):
        node = TextNode('This is a text node', TextType.ITALIC)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_missing_url_is_none(self):
        node = TextNode('None URL', TextType.LINK)
        self.assertIsNone(node.url)

    def test_not_TextNode(self):
        node = TextNode('This is a text node', TextType.BOLD)
        result = node.__eq__('not a text node')
        self.assertIs(result, NotImplemented)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None) # type: ignore[arg-type]
        self.assertEqual(html_node.value, "This is a text node") # type: ignore[arg-type]

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img") # type: ignore[arg-type]
        self.assertEqual(html_node.value, "") # type: ignore[arg-type]
        self.assertEqual(
            html_node.props, # type: ignore[arg-type]
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a") # type: ignore[arg-type]
        self.assertEqual(html_node.value, "This is a link") # type: ignore[arg-type]
        self.assertEqual(
            html_node.props, # type: ignore[arg-type]
            {"href": "https://www.boot.dev"},
        )

    def test_ignore_url(self):
        node = TextNode("This is bold", TextType.BOLD, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b") # type: ignore[arg-type]
        self.assertEqual(html_node.value, "This is bold") # type: ignore[arg-type]

    def test_code(self):
        node = TextNode('This is code', TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code') # type: ignore[arg-type]
        self.assertEqual(html_node.value, 'This is code') # type: ignore[arg-type]



if __name__ == "__main__":
    unittest.main()