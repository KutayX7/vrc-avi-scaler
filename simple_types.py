from typing import Any as _Any
from collections.abc import Callable

type Any = _Any

type ParameterValue = bool | int | float
type Height = float
type ScaleFactor = float
type TrackingType = int
type Callback = Callable[[str, Any], None]
