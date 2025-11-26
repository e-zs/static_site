#python

import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()