#python
import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type:TextType) -> list[TextNode]:
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

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Return list of (alt_text, url) for all markdown images in text."""
    matches = re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Return list of (alt_text, url) for all markdown links in text."""
    matches = re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        working_text = old_node.text
        extracted = extract_markdown_images(working_text)

        if not extracted:
            new_nodes.append(old_node)
            continue

        for node_text, node_link in extracted:
            sections = working_text.split(f'![{node_text}]({node_link})', 1)

            if len(sections) != 2:
                raise ValueError('invalid markdown, image section not closed')

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(node_text, TextType.IMAGE, node_link))

            working_text = sections[1] if len(sections) > 1 else ''

        if working_text:
            new_nodes.append(TextNode(working_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        working_text = old_node.text
        extracted = extract_markdown_links(working_text)

        if not extracted:
            new_nodes.append(old_node)
            continue

        for node_text, node_link in extracted:
            sections = working_text.split(f'[{node_text}]({node_link})', 1)

            if len(sections) != 2:
                raise ValueError('invalid markdown, link section not closed')

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(node_text, TextType.LINK, node_link))

            working_text = sections[1] if len(sections) > 1 else ''

        if working_text:
            new_nodes.append(TextNode(working_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    node = [TextNode(text, TextType.TEXT)]
    node = split_nodes_delimiter(node, '**', TextType.BOLD)
    node = split_nodes_delimiter(node, '_', TextType.ITALIC)
    node = split_nodes_delimiter(node, '`', TextType.CODE)
    node = split_nodes_image(node)
    node = split_nodes_link(node)

    return node