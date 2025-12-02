#python

import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    )

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

class TestExtractMarkdownImage(unittest.TestCase):
    def test_single_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        result = extract_markdown_images(text)
        self.assertListEqual([
            ('rick roll', 'https://i.imgur.com/aKaOqIh.gif')
            ],
            result
        )

    def test_multi_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertListEqual([
            ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
            ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg'),
            ],
            result
        )

    def test_no_image(self):
        text = 'This is a text with no image links!'
        result = extract_markdown_images(text)
        self.assertListEqual([], result)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        result = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")],
            result
        )

    def test_multi_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            result
        )

    def test_no_link(self):
        text = 'This is a text with no image links!'
        result = extract_markdown_links(text)
        self.assertListEqual([], result)

class TestSplitNodeImages(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestSplitNodeLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTextToTextnode(unittest.TestCase):
    def test_all_text_types(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            result
        )