from dataclasses import dataclass
from typing import Dict
from typing import List, Tuple, Set
from webserver.parser.base import parse_file_to_tree


import ast
from pathlib import Path


@dataclass
class NotationInstance:
    instance_name: str
    class_name: str
    args: List[str]


class NotationPipe:
    instances: Dict[str, NotationInstance]
    exec_orders: List[Tuple[str, str]]
    exec_instances: Set[str]

    def __init__(self) -> None:
        self.instances = {}
        self.exec_orders = []
        self.exec_instances = set()
    
    def add_instance(self, node: ast.Assign) -> None:
        assert isinstance(node.value, ast.Call)
        
        if isinstance(node.value.func, ast.Name):  # e.g: t1 = TaskA()                
            call_node = node.value # TaskA()
            # Get Class Name
            if isinstance(call_node.func, ast.Name):
                cls_name = call_node.func.id  # TaskA
            elif isinstance(call_node.func, ast.Attribute):
                cls_name = ast.unparse(call_node.func)
            else:
                return

            # unpack args
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            inst_name = names[0] if names else ""

            args_list = [ast.unparse(a) for a in call_node.args]
            args_list.extend(
                [f"{kw.arg}={ast.unparse(kw.value)}" for kw in call_node.keywords if kw.arg]
            )

            self.instances[inst_name] = NotationInstance(
                instance_name=inst_name, 
                class_name=cls_name, 
                args=args_list
            )
    
    def add_exec_orders(self, node: ast.BinOp) -> None:
        left = node.left.id if isinstance(node.left, ast.Name) else None
        right = node.right.id if isinstance(node.right, ast.Name) else None
        
        if left and right:
            self.exec_instances.add(left)
            self.exec_instances.add(right)
            if isinstance(node.op, ast.RShift):
                self.exec_orders.append((left, right))
            elif isinstance(node.op, ast.LShift):
                self.exec_orders.append((right, left))


def parse_pipeline_new(path: Path) -> NotationPipe:
    tree = parse_file_to_tree(path)
    notation_pipe = NotationPipe()

    # 1. collect variable -> class mapping
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            notation_pipe.add_instance(node)

    # 2. collect byte calculation dependency
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.RShift, ast.LShift)):
            notation_pipe.add_exec_orders(node)

    return notation_pipe