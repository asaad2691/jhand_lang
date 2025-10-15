# astnode.py
from typing import List, Optional

class ASTNode:
    """
    ASTNode represents a node in the Abstract Syntax Tree (AST) for JHAND language.
    Each node has a type, an optional value, and optional children nodes.
    """
    def __init__(self, nodetype: str, value=None, children: Optional[List["ASTNode"]] = None):
        self.nodetype = nodetype           # e.g., "Program", "Class", "Function", "Block", "Expr", "Print"
        self.value = value                 # can be string, dict, or any other info depending on node type
        self.children = children or []     # list of ASTNode children

    def add_child(self, child: "ASTNode"):
        """Add a child node to this AST node."""
        self.children.append(child)

    def __repr__(self):
        return f"ASTNode({self.nodetype}, {self.value}, children={len(self.children)})"
