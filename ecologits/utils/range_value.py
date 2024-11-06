from typing import Any, Union

from pydantic import BaseModel, model_validator
from typing_extensions import Self


class RangeValue(BaseModel):
    """
    RangeValue data model to represent intervals.

    Attributes:
        min: Lower bound of the interval.
        max: Upper bound of the interval.
    """
    min: float
    max: float

    @model_validator(mode="after")
    def check_order(self) -> Self:
        if self.min > self.max:
            raise ValueError("min value must be lower than max value")
        return self

    def __add__(self, other: Any) -> "RangeValue":
        if isinstance(other, RangeValue):
            return RangeValue(
                min=self.min + other.min,
                max=self.max + other.max,
            )
        else:
            return RangeValue(
                min=self.min + other,
                max=self.max + other
            )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, RangeValue):
            return self.min == other.min and self.max == other.max
        else:
            return self.min == other and self.max == other

    def __le__(self, other: Any) -> bool:
        if isinstance(other, RangeValue):
            return self.max <= other.max
        else:
            return self.max <= other

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, RangeValue):
            return self.max < other.min
        else:
            return self.max < other

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, RangeValue):
            return self.min >= other.min
        else:
            return self.min >= other

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, RangeValue):
            return self.min > other.max
        else:
            return self.min > other

    def __format__(self,format_spec:str)-> str:
        return f"{format(self.min,format_spec)} to {format(self.max,format_spec)}"




ValueOrRange = Union[int, float, RangeValue]
