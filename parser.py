from pydantic import BaseModel
import ast, pathlib, os
from typing import Tuple, List


class Method(BaseModel):
    name: str
    args: list[str]

class ClassInfo(BaseModel):
    file: str
    qualname: str
    bases: list[str]
    doc: str | None
    methods: list[Method]

class Pipeline:
    def __init__(self):
        self.edges = []

    def add(self, edge):
        self.edges.append(edge)

    def __repr__(self):
        return f"Pipeline(edges={self.edges})"

def parse_py(path: pathlib.Path) -> list[ClassInfo]:
    src = path.read_text(encoding="utf-8", errors="ignore")
    tree = ast.parse(src, filename=str(path))
    out = []
    for node in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
        bases = [ast.unparse(b) if hasattr(ast, "unparse") else getattr(getattr(b, "id", ""), "id", "") for b in node.bases]
        doc = ast.get_docstring(node)
        methods = []
        for n in node.body:
            if isinstance(n, ast.FunctionDef):
                args = [a.arg for a in n.args.args]  # 包含 self
                methods.append(Method(name=n.name, args=args))
        out.append(ClassInfo(
            file=str(path),
            qualname=node.name,
            bases=bases,
            doc=doc,
            methods=methods
        ))
    return out


def parse_pipeline(path: pathlib.Path) -> Pipeline:
    pipe = Pipeline()
    src = path.read_text(encoding="utf-8", errors="ignore")
    tree = ast.parse(src, filename=str(path))

    # 1. 收集变量 -> 类名的映射
    var_to_class = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):  # 例子: t1 = TaskA()
                class_name = node.value.func.id
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_to_class[target.id] = class_name

    # 2. 收集位运算依赖
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


def get_var_class(n: ast.AST, mapping: dict):
    """从变量映射拿类名"""
    if isinstance(n, ast.Name):
        return mapping.get(n.id)
    elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
        return n.func.id  # 直接类名
    return None