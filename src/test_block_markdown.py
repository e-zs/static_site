#python

import unittest
from block_markdown import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_paragraph(self):
        md = '''
This is a single paragraph
'''
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                'This is a single paragraph',
            ]
        )
    
    def test_blocks_split_on_single_line(self):
        md = '''
        First paragraph

Second paragraph
'''
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                'First paragraph',
                'Second paragraph',
            ]
        )
    
    def test_ignore_leading_blank_line(self):
        md = '''

 Paragraph after a leading empty line
'''
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                'Paragraph after a leading empty line',
            ]
        )

    def test_ignore_trailing_blank_line(self):
        md = '''
 Paragraph before a trailing empty line

 '''
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                'Paragraph before a trailing empty line',
            ]
        )

    def test_ignore_multiple_blank_lines(self):
        md = '''
Paragraph before multiple lines


Paragraph after multiple lines
'''
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                'Paragraph before multiple lines',
                'Paragraph after multiple lines',
            ]
        )

    def test_line_with_single_newline(self):
        md = '''
This is the first line
This is the second line right after the first
'''
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                'This is the first line\nThis is the second line right after the first',
            ]
        )

    def test_formated_lines(self):
        md = '''
This is a line with **bold** and _italic_ and a `code block`

- This is the first list item
- And this is the second list item

- And a new list with a new list item
'''
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                'This is a line with **bold** and _italic_ and a `code block`',
                '- This is the first list item\n- And this is the second list item',
                '- And a new list with a new list item',
            ]
        )