from fastapi import FastAPI
from parser import parse_py
from pydantic import BaseModel
import pathlib

class ClassPath(BaseModel):
    path: str

app = FastAPI()


@app.post('/parse_code')
def parse_code(class_path: ClassPath):
    input_path = pathlib.Path(class_path.path)

    print(input_path)
    if not input_path.exists():
        return {"error": "Path not exists"}

    class_list = parse_py(input_path)
    class_names = [c.qualname for c in class_list]

    return {"classes": class_names}