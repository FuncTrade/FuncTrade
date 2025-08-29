from unittest import TestCase
from webserver.parser.class_info import ClassInfo, parse_py
from webserver.parser.base import parse_file_to_tree
import os
from pathlib import Path
import ast


class TestParsePyClassInfo(TestCase):
    def test_class_info_from_def(self):
        example_path = os.path.relpath('webserver/tests/example_instance.py')
        example_path = Path(example_path)
        tree = parse_file_to_tree(example_path)

        nodes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
        node = nodes[0]

        if isinstance(node, ast.ClassDef):
            cls_info = ClassInfo.from_class_def(node, example_path)
            self.assertEqual(
                cls_info.to_info_dict(),
                {
                    "classname": "MACalculator",
                    "init_args": {"label": "str"}
                }
            )
        else:
            raise
    
    def test_parse_py(self):
        example_path = os.path.relpath('webserver/tests/example_instance.py')
        example_path = Path(example_path)

        result = parse_py(example_path)

        self.assertEqual(len(result), 1)

        self.assertEqual(
            result[0].to_info_dict(),
            {
                "classname": "MACalculator",
                "init_args": {"label": "str"}
            }
        )
