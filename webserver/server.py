from pathlib import Path
from fastapi import FastAPI
from webserver.parser.class_info import parse_py
from webserver.parser.pipeline import parse_pipeline
from webserver.parser.base import search_target_dir
from pydantic import BaseModel
import pathlib
from typing import Dict, List

class ClassPath(BaseModel):
    path: str

app = FastAPI()


@app.post('/api/parse_code')
def parse_code(class_path: ClassPath):
    input_path = pathlib.Path(class_path.path)

    if not input_path.exists():
        return {"error": "Path not exists"}

    class_list = parse_py(input_path)
    class_names = [{"class": c.qualname} for c in class_list]

    edges = parse_pipeline(input_path).edges

    return {"classes": class_names, "edges": edges}

@app.get('/api/default_classes')
def get_default_classes() -> Dict:
    current_path = pathlib.Path(__file__).resolve()
    function_path = current_path.parent.parent.joinpath('function')
    default_classes = []

    for p in search_target_dir(function_path):
        default_classes.extend(parse_py(p))

    class_names = [{"class": c.qualname} for c in default_classes]

    return {"default_classes": class_names}



