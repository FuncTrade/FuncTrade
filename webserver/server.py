from fastapi import FastAPI
from webserver.parser import parse_py, parse_pipeline
from pydantic import BaseModel
import pathlib

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
