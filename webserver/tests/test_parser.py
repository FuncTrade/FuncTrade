from unittest import TestCase
from webserver.parser import parse_py, parse_pipeline
import os
import pathlib


class TestParser(TestCase):
    def test_parse_py(self):
        example_path = os.path.relpath('webserver/tests/example_model.py')
        example_path = pathlib.Path(example_path)
        results = parse_py(example_path)

        self.assertEqual(len(results), 2)
        self.assertEqual([c.qualname for c in results], ['DataFeed','Actor'])
    
    def test_parse_pipeline(self):
        example_path = os.path.relpath('webserver/tests/example_model.py')
        example_path = pathlib.Path(example_path)
        results = parse_pipeline(example_path)

        self.assertEqual(results.edges, [('DataFeed', 'Actor')])