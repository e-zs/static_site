#python

class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError('not implemented yet')

    def props_to_html(self):
        if not self.props:
            return ''    
        return ' ' + ' '.join(f'{k}="{v}"' for k, v in self.props.items())
    
    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict | None = None) -> None:
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        # return super().to_html() # Include if I want to keep the parent logic?
        if self.value is None:
            raise ValueError('no value provided')
        if self.tag is None:
            return self.value
        html_props = self.props_to_html()
        start_tag = f'<{self.tag}{html_props}>'
        end_tag = f'</{self.tag}>'

        return f'{start_tag}{self.value}{end_tag}'
    
    def __repr__(self) -> str:
        return f'LeafNode({self.tag}, {self.value}, {self.props})'