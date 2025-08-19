from pathlib import Path
from typing import List, Dict, Tuple, Any, Sequence, TypedDict, Union
from dataclasses import dataclass


ParamValue = Union[str, int, float, bool]

@dataclass
class InstanceDef:
    classname: str
    module: str
    params: Dict[str, ParamValue]

    @classmethod
    def from_dict(cls, d: Dict) -> 'InstanceDef':
        return cls(
            classname=d['classname'],
            module=d['module'],
            params=d['params']
        )

@dataclass
class InstanceCall:
    source: str
    target: str

    @classmethod
    def from_dict(cls, d: Dict) -> 'InstanceCall':
        return cls(
            source=d['source'],
            target=d['target']
        )


def generate_pipeline_code(classes: Sequence[InstanceDef], edges: Sequence[InstanceCall], output_path: Path):
    """
    Example:

    data = {
        "classes": [
            {"classname": "DataFeed", "module": "lib.data", "params": {"path": "data.csv"}},
            {"classname": "Actor", "module": "lib.actor", "params": {"name": "main"}}
        ],
        "edges": [["DataFeed", "Actor"]]
    }
    """
    lines = []
    imports = {}

    # 1. 生成 import 语句
    for c in classes:
        imports.setdefault(c.module, []).append(c.classname)
    for module, cls_list in imports.items():
        lines.append(f"from {module} import {', '.join(cls_list)}")
    lines.append("")

    # 2. 实例化对象
    for c in classes:
        var_name = c.classname.lower()
        params = ", ".join(f"{k}={repr(v)}" for k, v in c.params.items())
        lines.append(f"{var_name} = {c.classname}({params})")
    lines.append("")

    # 3. 定义 edges
    for edge in edges:
        left, right = edge.source, edge.target
        lines.append(f"{left.lower()} >> {right.lower()}")

    code = "\n".join(lines)
    output_path.write_text(code, encoding="utf-8")
    return code
    
