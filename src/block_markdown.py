#python

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split('\n\n')
    markdown_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        markdown_blocks.append(block)

    return markdown_blocks