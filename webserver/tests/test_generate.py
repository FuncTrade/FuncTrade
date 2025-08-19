from unittest import TestCase
from webserver.generate import generate_pipeline_code, InstanceDef, InstanceCall


class TestGenerate(TestCase):
    def test_generate_pipeline_code(self):
        data = {
            "classes": [
                {"classname": "DataFeed", "module": "lib.data", "params": {"path": "data.csv"}},
                {"classname": "Actor", "module": "lib.actor", "params": {"name": "main"}}
            ],
            "edges": [{"source": "DataFeed", "target": "Actor"}]
        }
        classes = [InstanceDef.from_dict(d) for d in data["classes"]]
        edges = [InstanceCall.from_dict(e) for e in data["edges"]]

        code = generate_pipeline_code(classes, edges)
        
        desired_output = ""
        
        desired_output+="from lib.data import DataFeed\n"
        desired_output+="from lib.actor import Actor\n\n"
        desired_output+="datafeed = DataFeed(path='data.csv')\n"
        desired_output+="actor = Actor(name='main')\n\n"
        desired_output+="datafeed >> actor"

        self.assertEqual(code, desired_output)