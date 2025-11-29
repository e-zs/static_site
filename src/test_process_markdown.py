#python

import unittest

from textnode import TextNode, TextType
from process_markdown import split_nodes_delimiter

class TestSplitMarkdownNode(unittest.TestCase):
    def test_not_text(self):
        node = [TextNode('This is not **TextNode.TEXT**', TextType.BOLD)]
        result = split_nodes_delimiter(node, '**', TextType.BOLD)
        self.assertEqual(result[0].text, 'This is not **TextNode.TEXT**')
        self.assertEqual(result[0].text_type, TextType.BOLD)

    # TODO: More tests
    # Multiple formated words
    # Multiple different formating in the same input
    # Multiple words within the same delimiter
    # Test each formating (bold, code, italic, )

    def test_texttype_code(self):
        node = [TextNode('This is a text with a `code block` word', TextType.TEXT)]
        result = split_nodes_delimiter(node, '`', TextType.CODE)
        print('result', result)

    def test_odd_delimiters(self):
        node = [TextNode('This is a text with an *uneven* *number of delimiters', TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(node, '*', TextType.BOLD)