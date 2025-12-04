#python

import unittest
from block_markdown import BlockType
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    )

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

    def test_ignore_two_blank_lines(self):
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

    def test_ignore_three_blank_lines(self):
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

    def test_empty(self):
        md = ''''''
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [

            ]
        )

    def test_whitespace(self):
        md = '''

'''
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [

            ]
        )

class TestBlockToBlock(unittest.TestCase):
    def test_empty(self):
        md = ''''''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_heading(self):
        md = '# Level one heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)
        md = '## Level two heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)
        md = '### Level three heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)
        md = '#### Level four heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)
        md = '##### Level five heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)
        md = '###### Level six heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)
        md = '####### Level seven heading'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)
        md = '''# First level
And a new line that is not a heading
'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_code(self):
        md = '''```This is a code block```'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.CODE)

        md = '''```This is a code block
with a new line

and another new line
```'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.CODE)

        md = '''```This is a code block
with a new line```

and data after the code block
'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_quote(self):
        md = '''>A single quoted line'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.QUOTE)

        md = '''>A single quoted line'
>Followed by another'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.QUOTE)

        md = '''>A single quoted line'
Followed by a non-quoted line'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_unordered_list(self):
        md = '''- Single list item'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

        md = '''- First list item
- Second list item
'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

        md = '''- First list item
-Not a list item
'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_ordered_list(self):
        md = '''1. Only one list item'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.ORDERED_LIST)

        md = '''1. First list item
2. Second list item
3. Third list item
'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.ORDERED_LIST)

        md = '''1. First list item
3. Second list item out of order
4. Third list item
'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

        md = '''1. First list item
2Not a list item
'''
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)