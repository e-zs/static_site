#python
import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type:TextType):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        node_parts = old_node.text.split(delimiter)

        if len(node_parts) == 1:
            new_nodes.append(old_node)
            continue
        elif len(node_parts) % 2 == 0:
            raise Exception(f'Error: odd number of delimiters in: {old_node.text}')
        else:
            for i, node_part in enumerate(node_parts):
                if node_part == '':
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(node_part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(node_part, text_type))
                    
    return new_nodes

def extract_markdown_images(text):
    """Return list of (alt_text, url) for all markdown images in text."""
    matches = re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    return matches

def extract_markdown_links(text):
    """Return list of (alt_text, url) for all markdown links in text."""
    matches = re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    return matches