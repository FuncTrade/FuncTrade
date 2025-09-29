from .example_class_info import MACalculator
from base_function.base import Pipeline

pipe = Pipeline()

ma_example = MACalculator('ma_example', pipeline=pipe)

ma_example2 = MACalculator(label='ma_example2', pipeline=pipe)