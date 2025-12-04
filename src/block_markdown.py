#python

from enum import Enum
import re

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split('\n\n')
    markdown_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        markdown_blocks.append(block)

    return markdown_blocks

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(markdown_block: str) -> BlockType:
    if re.match(r'^[#]{1,6}\s[^\n]+$', markdown_block):
        return BlockType.HEADING
    if re.match(r'(?s)^```.*```$', markdown_block):
        return BlockType.CODE
    if re.fullmatch(r'(?:>.*(?:\n|$))+', markdown_block):
        return BlockType.QUOTE
    if re.fullmatch(r'(?:- .*(?:\n|$))+', markdown_block):
        return BlockType.UNORDERED_LIST
    if is_ordered_numbered_list(markdown_block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def is_ordered_numbered_list(s: str) -> bool:
    lines = s.splitlines()
    if not lines:
        return False
    pat = re.compile(r'^(\d+)\.\s')
    for i, line in enumerate(lines, start=1):
        m = pat.match(line)
        if not m:
            return False
        if int(m.group(1)) != i:
            return False
    return True