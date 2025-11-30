#python

import unittest

from textnode import TextNode, TextType
from process_markdown import split_nodes_delimiter

class TestSplitMarkdownNode(unittest.TestCase):
    def test_not_text_node(self):
        node = [TextNode('This is not **TextNode.TEXT**', TextType.BOLD)]
        result = split_nodes_delimiter(node, '**', TextType.BOLD)
        self.assertEqual(result[0].text, 'This is not **TextNode.TEXT**')
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_multiple_formated_words(self):
        node = [TextNode('This is two **bold** **words**', TextType.TEXT)]
        result = split_nodes_delimiter(node, '**', TextType.BOLD)
        self.assertListEqual(
            [
                TextNode('This is two ', TextType.TEXT, None),
                TextNode('bold', TextType.BOLD, None),
                TextNode(' ', TextType.TEXT, None),
                TextNode('words', TextType.BOLD, None),
            ],
            result
        )

    def test_words_different_format(self):
        node = [TextNode('This is a **bold** and an _italic_ word', TextType.TEXT)]
        result = split_nodes_delimiter(node, '_', TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode('This is a **bold** and an ', TextType.TEXT, None),
                TextNode('italic', TextType.ITALIC, None),
                TextNode(' word', TextType.TEXT, None),
            ],
            result
        )

    def test_format_multiple_words(self):
        node = [TextNode('This is multiple **bold words** together', TextType.TEXT)]
        result = split_nodes_delimiter(node, '**', TextType.BOLD)
        self.assertListEqual(
            [
                TextNode('This is multiple ', TextType.TEXT, None),
                TextNode('bold words', TextType.BOLD, None),
                TextNode(' together', TextType.TEXT, None),
            ],
            result
        )
    
    def test_multiple_nodes(self):
        node = [
            TextNode('First node with **bold** formating', TextType.TEXT),
            TextNode('Second node with _italic_ and **bold** formating', TextType.TEXT)
        ]
        result = split_nodes_delimiter(node, '**', TextType.BOLD)
        self.assertListEqual(
            [
                TextNode('First node with ', TextType.TEXT, None),
                TextNode('bold', TextType.BOLD, None),
                TextNode(' formating', TextType.TEXT, None),
                TextNode('Second node with _italic_ and ', TextType.TEXT, None),
                TextNode('bold', TextType.BOLD, None),
                TextNode(' formating', TextType.TEXT, None),
            ],
            result
        )

    def test_texttype_code(self):
        node = [TextNode('This is a text with a `code block` word', TextType.TEXT)]
        result = split_nodes_delimiter(node, '`', TextType.CODE)
        self.assertListEqual(
            [
                TextNode('This is a text with a ', TextType.TEXT, None),
                TextNode('code block', TextType.CODE, None),
                TextNode(' word', TextType.TEXT, None),
            ],
            result
        )

    def test_odd_delimiters(self):
        node = [TextNode('This is a text with an *uneven* *number of delimiters', TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(node, '*', TextType.BOLD)

    def test_all_formated(self):
        node = [TextNode('_This is all italic_', TextType.TEXT)]
        result = split_nodes_delimiter(node, '_', TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode('This is all italic',TextType.ITALIC, None)
            ],
            result
        )

    def test_start_end_formated(self):
        node = [TextNode('`code block` at start and `at end`', TextType.TEXT)]
        result = split_nodes_delimiter(node, '`', TextType.CODE)
        self.assertListEqual(
            [
            TextNode('code block', TextType.CODE, None),
            TextNode(' at start and ', TextType.TEXT, None),
            TextNode('at end', TextType.CODE, None),
            ],
            result
        )