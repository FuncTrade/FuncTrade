import ast
from pathlib import Path
from typing import List


def parse_file_to_tree(path: Path) -> ast.Module:
    src = path.read_text(encoding="utf-8", errors="ignore")
    tree = ast.parse(src, filename=str(path))
    return tree

def search_target_dir(target_dir: Path) -> List[Path]:
    if not target_dir.exists() or not target_dir.is_dir():
        return []
    return list(target_dir.rglob("*.py"))