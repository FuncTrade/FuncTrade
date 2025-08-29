from pydantic import BaseModel
import ast
from pathlib import Path
from webserver.parser.base import parse_file_to_tree
from typing import Optional, Union, Dict

class Argument(BaseModel):
    name: str
    typehint: str | None

class Method(BaseModel):
    name: str
    args: list[Argument]

class ClassInfo(BaseModel):
    file: str
    qualname: str
    bases: list[str]
    doc: str | None
    methods: list[Method]

    def to_info_dict(self) -> Dict[str, Union[str, Dict[str, Optional[str]]]]:
        """
        Return dict: {"classname": classname, "init_args": {arg_name: arg_type}}
        only for __init__ method
        """
        init_method = next((m for m in self.methods if m.name == "__init__"), None)
        sig_dict = {"classname": self.qualname, "init_args": {}}
        if init_method:
            sig_dict["init_args"] = {arg.name: arg.typehint for arg in init_method.args if arg.name != "self"}
        return sig_dict
    
    @classmethod
    def from_class_def(cls, node: ast.ClassDef, path: Path) -> 'ClassInfo':
        bases = [ast.unparse(b) if hasattr(ast, "unparse") else getattr(getattr(b, "id", ""), "id", "") for b in node.bases]
        doc = ast.get_docstring(node)
        methods = []
        for n in node.body:
            if isinstance(n, ast.FunctionDef):
                args = []
                for a in n.args.args:
                    typehint = ast.unparse(a.annotation) if a.annotation is not None else None
                    args.append(Argument(name=a.arg, typehint=typehint))
                methods.append(Method(name=n.name, args=args))
        return cls(
            file=str(path),
            qualname=node.name,
            bases=bases,
            doc=doc,
            methods=methods
        )

def parse_py(path: Path) -> list[ClassInfo]:
    tree = parse_file_to_tree(path)
    out = []
    for node in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
        out.append(ClassInfo.from_class_def(node, path))
    return out