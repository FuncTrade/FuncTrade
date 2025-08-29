from .class_info import ClassInfo
from pydantic import BaseModel
from typing import Optional, Dict, Union, List
import ast
from pathlib import Path
from .base import parse_file_to_tree


class Instance(BaseModel):
    name: str
    class_info: ClassInfo
    args: List[str]

    def to_info_dict(self) -> Dict[str, Union[str, Dict[str, Optional[str]], List[str]]]:
        """
        Return dict: {"name": name, "classname": classname, "init_args": {arg_name: arg_type}, "init_values": [arg_value, ..]}
        only for __init__ method
        """
        class_info = self.class_info.to_info_dict()

        results = {
            "name": self.name,
            "classname": class_info['classname'],
            "init_args": class_info['init_args'],
            "init_values": self.args
        }

        return results


def parse_instances(path: Path, classes: list[ClassInfo]) -> list[Instance]:
    tree = parse_file_to_tree(path)
    instances = []

    class_lookup = {c.qualname: c for c in classes}

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            call_node = node.value
            # Get Class Name
            if isinstance(call_node.func, ast.Name):
                cls_name = call_node.func.id
            elif isinstance(call_node.func, ast.Attribute):
                cls_name = ast.unparse(call_node.func)
            else:
                continue

            if cls_name in class_lookup:
                # unpack args
                names = [t.id for t in node.targets if isinstance(t, ast.Name)]
                inst_name = names[0] if names else ""

                args_list = [ast.unparse(a) for a in call_node.args]
                args_list.extend(
                    [f"{kw.arg}={ast.unparse(kw.value)}" for kw in call_node.keywords if kw.arg]
                )

                instances.append(
                    Instance(name=inst_name, class_info=class_lookup[cls_name], args=args_list)
                )
    return instances

