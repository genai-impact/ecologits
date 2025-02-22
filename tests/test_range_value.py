import pytest
import operator

from ecologits.utils.range_value import RangeValue

def test_range_formats_ok():
    range = RangeValue(min =0.00000006, max=0.00008)
    expected = f"{range.min:.2f} to {range.max:.2f}"
    assert f"{range:.2f}" == expected


@pytest.mark.parametrize("val_1,val_2,op,result", [
    (RangeValue(min=1, max=2), RangeValue(min=1, max=2), operator.eq, True),
    (RangeValue(min=1, max=2), RangeValue(min=1, max=3), operator.eq, False),
    (RangeValue(min=1, max=2), RangeValue(min=2, max=3), operator.eq, False),
    (RangeValue(min=1, max=2), RangeValue(min=1, max=3), operator.ne, True),
    (RangeValue(min=1, max=2), RangeValue(min=2, max=3), operator.ne, True),
    (RangeValue(min=1, max=2), RangeValue(min=1, max=2), operator.ne, False),
    (RangeValue(min=0, max=1), RangeValue(min=2, max=3), operator.le, True),
    (RangeValue(min=0, max=1), RangeValue(min=2, max=3), operator.lt, True),
    (RangeValue(min=2, max=3), RangeValue(min=0, max=1), operator.ge, True),
    (RangeValue(min=2, max=3), RangeValue(min=0, max=1), operator.gt, True),
    (RangeValue(min=0, max=1), RangeValue(min=1, max=2), operator.le, True),
    (RangeValue(min=0, max=1), RangeValue(min=1, max=2), operator.lt, False),
    (RangeValue(min=1, max=2), RangeValue(min=0, max=1), operator.ge, True),
    (RangeValue(min=1, max=2), RangeValue(min=0, max=1), operator.gt, False),
    (RangeValue(min=1.5, max=2), RangeValue(min=1, max=2), operator.ge, True),
    (RangeValue(min=1.5, max=2), RangeValue(min=1, max=2), operator.gt, False),
    (RangeValue(min=1, max=2), RangeValue(min=1.5, max=2), operator.le, True),
    (RangeValue(min=1, max=2), RangeValue(min=1.5, max=2), operator.lt, False),
    (RangeValue(min=0, max=1.5), RangeValue(min=1, max=2), operator.le, True),
    (RangeValue(min=0, max=1.5), RangeValue(min=1, max=2), operator.lt, False),
    (RangeValue(min=1, max=2), RangeValue(min=0, max=1.5), operator.ge, True),
    (RangeValue(min=1, max=2), RangeValue(min=0, max=1.5), operator.gt, False),
    (RangeValue(min=1, max=1), 1, operator.eq, True),
    (RangeValue(min=1, max=2), 1, operator.eq, False),
    (RangeValue(min=1, max=2), 2, operator.eq, False),
    (RangeValue(min=1, max=2), 1, operator.ne, True),
    (RangeValue(min=2, max=3), 1, operator.ne, True),
    (RangeValue(min=1, max=1), 1, operator.ne, False),
    (RangeValue(min=1, max=2), 1.5, operator.ge, False),
    (RangeValue(min=1, max=2), 0.5, operator.ge, True),
    (1.5, RangeValue(min=1, max=2), operator.le, False),
    (0.5, RangeValue(min=1, max=2), operator.le, True),
    (RangeValue(min=1, max=2), 1, operator.ge, True),
    (RangeValue(min=1, max=2), 0, operator.ge, True),
    (1, RangeValue(min=1, max=2), operator.le, True),
    (0, RangeValue(min=1, max=2), operator.le, True),
    (RangeValue(min=-2, max=-1), -1.5, operator.ge, False),
    (RangeValue(min=-2, max=-1), -2.5, operator.ge, True),
    (-1.5, RangeValue(min=-2, max=-1), operator.le, False),
    (-2.5, RangeValue(min=-2, max=-1), operator.le, True),
])
def test_value_range_compare(val_1, val_2, op, result):
    assert op(val_1, val_2) == result


@pytest.mark.parametrize("val_1,val_2,op,exp_result", [
    (RangeValue(min=1, max=2), RangeValue(min=1, max=2), operator.add, RangeValue(min=2, max=4)),
    (RangeValue(min=1, max=2), 1, operator.add, RangeValue(min=2, max=3)),
    (RangeValue(min=1, max=2), 2, operator.mul, RangeValue(min=2, max=4)),
    (RangeValue(min=2, max=4), 2, operator.truediv, RangeValue(min=1, max=2)),
])
def test_value_range_transformation(val_1, val_2, op, exp_result):
    result = op(val_1, val_2)
    assert result.min == exp_result.min and result.max == exp_result.max
