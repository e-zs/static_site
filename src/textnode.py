#python

from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (self.text, self.text_type, self.url) == (other.text, other.text_type, other.url)
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
    


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if not isinstance(text_node.text_type, TextType):
        raise Exception('Error: unknown text type')
    if text_node.text_type == TextType.TEXT:
        node = LeafNode(None, text_node.text, None)
        return node
    elif text_node.text_type == TextType.BOLD:
        node = LeafNode('b', text_node.text, None)
        return node
    elif text_node.text_type == TextType.ITALIC:
        node = LeafNode('i', text_node.text, None)
        return node
    elif text_node.text_type == TextType.CODE:
        node = LeafNode('code', text_node.text, None)
        return node
    elif text_node.text_type == TextType.LINK:
        prop = {'href': text_node.url}
        node = LeafNode('a', text_node.text, prop)
        return node
    elif text_node.text_type == TextType.IMAGE:
        prop = {
            'src': text_node.url,
            'alt': text_node.text,
        }
        node = LeafNode('img', '', prop)
        return node
    
    raise TypeError(f'Unepexted text_type: {text_node.text_type}')