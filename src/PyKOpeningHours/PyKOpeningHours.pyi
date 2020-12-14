from typing import Any

class Error():
    EvaluationError: Any = ...
    IncompatibleMode: Any = ...
    MissingLocation: Any = ...
    MissingRegion: Any = ...
    NoError: Any = ...
    Null: Any = ...
    SyntaxError: Any = ...
    UnsupportedFeature: Any = ...
    names: Any = ...
    values: Any = ...

class Mode():
    IntervalMode: Any = ...
    PointInTimeMode: Any = ...
    names: Any = ...
    values: Any = ...

class OpeningHours():
    def error(KOpeningHours) -> Error: ...
    def normalizedExpression(self) -> str: ...
    def setExpression(self, str) -> None: ...