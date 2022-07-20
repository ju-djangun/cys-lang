from anytree import Node  # type: ignore


"""
ALT - Abstract Line Tree.
"""


class AbstractLineTreeManager:
    root_node: Node = None
    node_cursor: Node = None

    def __init__(self):
        """
        Create root and connect to root_node.
        When TreeManager is created, node_cursor is root.
        """
        root_data = {
            "line_no": -1,
            "indent_depth": -1,
            "is_last_colon": True,
        }
        root_node = self.create_node("root_0", "", root_data)
        self.root_node = root_node
        self.node_cursor = self.root_node

    def create_node(
        self, nodename: str, code: str, line_data: dict, parent: Node = None
    ) -> Node:
        """
        Create new node.
        """
        new_node = Node(nodename, data=code, line_data=line_data, parent=parent)
        return new_node

    def adopt_node(self, node: Node, parent: Node):
        node.parent = parent

    def get_cursor_indent(self) -> int:
        return self.node_cursor.line_data["indent_depth"]

    def get_cursor_parent(self) -> Node:
        return self.node_cursor.parent

    def get_cursor_pedigree(self) -> list:
        """
        return [node_cursor, parent, grandparent,... , root]
        """
        pedigree_list: list = []
        cursor_memo: Node = self.node_cursor
        pedigree_list.append(cursor_memo)
        while self.node_cursor != self.root_node:
            parent = self.node_cursor.parent
            pedigree_list.append(parent)
            self.node_cursor = parent
        self.node_cursor = cursor_memo
        return pedigree_list
