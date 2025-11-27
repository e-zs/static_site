#python

import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def setUp(self) -> None:
        self.node_children = [
            HTMLNode("li", "first list item"),
            HTMLNode("li", "second list item"),
        ]
        self.node_props = {
            'first': 'value',
            'second': 'value',
        }

    def test_all_input_types(self):
        node = HTMLNode('a tag', 'some value', self.node_children, self.node_props)
        self.assertIsInstance(node.tag, str)
        self.assertIsInstance(node.value, str)
        self.assertIsInstance(node.children, list)
        self.assertIsInstance(node.props, dict)

    def test_all_inputs(self):
        node = HTMLNode('a tag', 'some value', self.node_children, self.node_props)
   
        self.assertIs(node.children, self.node_children)
        self.assertIs(node.props, self.node_props)

    def test_repr(self):
        node = HTMLNode('a tag', 'some value', self.node_children, self.node_props)
        result = repr(node)
        self.assertIn('a tag', result)
        self.assertIn('some value', result)
        self.assertIn('HTMLNode', result)
    
    def test_props_to_html(self):
        node = HTMLNode('a tag', 'some value', self.node_children, self.node_props)
        self.assertEqual(node.props_to_html(), ' first="value" second="value"')

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_to_html_raises_error(self):
        node = HTMLNode("p", "text")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_nested_children(self):
        child_node = HTMLNode("span", "child")
        parent_node = HTMLNode("div", None, [child_node])
        if parent_node.children is not None:
            self.assertEqual(len(parent_node.children), 1)
            self.assertIsInstance(parent_node.children[0], HTMLNode)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode('p', 'Hello, world!')
        self.assertEqual(node.to_html(), '<p>Hello, world!</p>')

    def test_leaf_to_html_prop(self):
        node = LeafNode('a', 'Click me!', {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value_raises(self):
        node = LeafNode("p", None)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()