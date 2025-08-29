from unittest import TestCase
from webserver.parser.instance import parse_instances
from webserver.parser.class_info import ClassInfo, Method, Argument
import os
from pathlib import Path


class TestParseInstances(TestCase):
    def test_parse_instances(self):
        example_path = os.path.relpath('webserver/tests/example_instance.py')
        example_path = Path(example_path)
        classes = [
            ClassInfo(
                file="example_class_info",
                qualname="MACalculator",
                bases=[],
                doc=None,
                methods=[Method(name="__init__", args=[Argument(name="label", typehint="str")])]
            )]

        instances = parse_instances(example_path, classes)

        self.assertEqual(len(instances), 2)

        self.assertEqual(
            instances[0].to_info_dict(),
            {
                "name": "ma_example",
                "classname": "MACalculator",
                "init_args": {"label": "str"},
                "init_values": ["'ma_example'"]
            }
        )

        self.assertEqual(
            instances[1].to_info_dict(),
            {
                "name": "ma_example2",
                "classname": "MACalculator",
                "init_args": {"label": "str"},
                "init_values": ["label='ma_example2'"]
            }
        )