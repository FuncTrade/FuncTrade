from pathlib import Path
from fastapi import FastAPI
from webserver.parser.class_info import parse_py, ClassInfo
from webserver.parser.pipeline import parse_pipeline
from webserver.parser.base import search_target_dir
from webserver.parser.parser import parse_pipeline_new, NotationPipe
from pydantic import BaseModel
import pathlib
from typing import Dict, List

class TargetPath(BaseModel):
    path: str

app = FastAPI()


@app.post('/api/parse_code')
def parse_code(path: TargetPath):
    """
    All ClassInfo should be in Default Class Folder
    """
    pipeline_path = pathlib.Path(path.path)

    current_path = pathlib.Path(__file__).resolve()
    function_path = current_path.parent.parent.joinpath('function')
    default_classes: List[ClassInfo] = []

    for p in search_target_dir(function_path):
        default_classes.extend(parse_py(p))

    if not pipeline_path.exists():
        return {"error": "Path not exists"}

    class_names = [{"class": c.qualname} for c in default_classes]

    edges = parse_pipeline(pipeline_path).edges

    return {"classes": class_names, "edges": edges}

@app.post('/api/parse_code_new')
def parse_code_new(path: TargetPath):
    """
    All ClassInfo should be in Default Class Folder
    """
    pipeline_path = pathlib.Path(path.path)
    
    if not pipeline_path.exists():
        return {"error": "Path not exists"}
    
    notation_pipe = parse_pipeline_new(pipeline_path)

    class_names = [{"class": i} for i in notation_pipe.exec_instances]

    edges = notation_pipe.exec_orders

    return {"classes": class_names, "edges": edges}

@app.get('/api/default_classes')
def get_default_classes() -> Dict:
    current_path = pathlib.Path(__file__).resolve()
    function_path = current_path.parent.parent.joinpath('function')
    default_classes: List[ClassInfo] = []

    for p in search_target_dir(function_path):
        default_classes.extend(parse_py(p))

    class_names = [{"class": c.qualname} for c in default_classes]

    return {"default_classes": class_names}

@app.post('/api/list_pipeline')
def list_pipeline(dir_path: TargetPath) -> Dict:
    input_path = pathlib.Path(dir_path.path)

    if not input_path.exists():
        return {"error": "Path not exists"}
    
    pipeline_names = [{"pipeline": p.stem} for p in search_target_dir(input_path) if not p.stem.startswith("_")]
    
    return {"pipelines": pipeline_names}



