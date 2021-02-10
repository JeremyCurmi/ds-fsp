from sklearn import pipeline
from pkg.preprocessor import (
    transformers
)
preprocessing_pipe = pipeline.Pipeline(
    steps = [
        ("inputcleaner", transformers.InputCleaner()),
    ]
)