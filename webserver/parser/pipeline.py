from typing import List, Tuple, Optional
from webserver.parser.base import parse_file_to_tree


import ast
from pathlib import Path


def get_var_class(n: ast.AST, mapping: dict[str, str]) -> Optional[str]:
    """get classname from variable"""
    if isinstance(n, ast.Name):
        return mapping.get(n.id)
    elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
        return n.func.id  # Class Name
    return None


class NotationPipeline:
    edges: List[Tuple]

    def __init__(self):
        self.edges = []

    def add(self, edge):
        self.edges.append(edge)

    def __repr__(self):
        return f"Pipeline(edges={self.edges})"

def parse_pipeline(path: Path) -> NotationPipeline:
    pipe = NotationPipeline()
    tree = parse_file_to_tree(path)

    # 1. collect variable -> class mapping
    var_to_class = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):  # e.g: t1 = TaskA()
                class_name = node.value.func.id
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_to_class[target.id] = class_name

    # 2. collect byte calculation dependency
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.RShift, ast.LShift)):
            left = get_var_class(node.left, var_to_class)
            right = get_var_class(node.right, var_to_class)
            if left and right:
                if isinstance(node.op, ast.RShift):
                    pipe.add((left, right))
                elif isinstance(node.op, ast.LShift):
                    pipe.add((right, left))

    return pipe