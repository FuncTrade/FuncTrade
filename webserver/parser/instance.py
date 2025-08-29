from pydantic import BaseModel


import ast
from pathlib import Path

from webserver.parser.base import parse_file_to_tree


class Method(BaseModel):
    name: str
    args: list[str]


class ClassInfo(BaseModel):
    file: str
    qualname: str
    bases: list[str]
    doc: str | None
    methods: list[Method]

def parse_py(path: Path) -> list[ClassInfo]:
    tree = parse_file_to_tree(path)
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