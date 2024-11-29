import operator

import pytest

from ecologits.impacts.modeling import BaseImpact, Energy, GWP, ADPe, PE
from ecologits.exceptions import ModelingError
from ecologits.utils.range_value import RangeValue


impact_config = dict(
    type="test",
    name="Test",
    unit=""
)


@pytest.mark.parametrize('impact_1,impact_2,result', [
    (
            BaseImpact(**impact_config, value=1),
            BaseImpact(**impact_config, value=1),
            BaseImpact(**impact_config, value=2)
    ),
    (
            BaseImpact(**impact_config, value=RangeValue(min=1, max=2)),
            BaseImpact(**impact_config, value=1),
            BaseImpact(**impact_config, value=RangeValue(min=2, max=3))
    ),
    (
            BaseImpact(**impact_config, value=RangeValue(min=1, max=2)),
            BaseImpact(**impact_config, value=RangeValue(min=1, max=2)),
            BaseImpact(**impact_config, value=RangeValue(min=2, max=4))
    ),
    (Energy(value=1), Energy(value=1), Energy(value=2)),
    (GWP(value=1), GWP(value=1), GWP(value=2)),
    (ADPe(value=1), ADPe(value=1), ADPe(value=2)),
    (PE(value=1), PE(value=1), PE(value=2)),
])
def test_impact_add(impact_1, impact_2, result):
    impact_sum = impact_1 + impact_2
    assert impact_sum == result


@pytest.mark.parametrize('impact_1,impact_2', [
    (BaseImpact(**impact_config, value=1), BaseImpact(type="other", name="Other", value=1, unit="")),
    (BaseImpact(**impact_config, value=RangeValue(min=1, max=2)), BaseImpact(type="other", name="Other", value=1, unit="")),
    (BaseImpact(**impact_config, value=RangeValue(min=1, max=2)),
     BaseImpact(type="other", name="Other", value=RangeValue(min=1, max=2), unit="")),
    (Energy(value=1), GWP(value=1)),
    (Energy(value=1), ADPe(value=1)),
    (Energy(value=1), PE(value=1)),
    (GWP(value=1), ADPe(value=1)),
    (GWP(value=1), PE(value=1)),
    (ADPe(value=1), PE(value=1)),
])
def test_impact_cannot_add(impact_1, impact_2):
    with pytest.raises(ModelingError):
        impact_1 + impact_2


@pytest.mark.parametrize('impact_1,impact_2,op', [
    (BaseImpact(**impact_config, value=1), BaseImpact(**impact_config, value=1), operator.eq),
    (BaseImpact(**impact_config, value=1), BaseImpact(**impact_config, value=2), operator.lt),
    (BaseImpact(**impact_config, value=2), BaseImpact(**impact_config, value=2), operator.le),
    (BaseImpact(**impact_config, value=2), BaseImpact(**impact_config, value=2), operator.ge),
    (BaseImpact(**impact_config, value=2), BaseImpact(**impact_config, value=1), operator.gt),
    (BaseImpact(**impact_config, value=2), BaseImpact(**impact_config, value=1), operator.ne),

    (BaseImpact(**impact_config, value=RangeValue(min=1, max=1)), BaseImpact(**impact_config, value=1), operator.eq),
    (BaseImpact(**impact_config, value=RangeValue(min=1, max=2)), BaseImpact(**impact_config, value=3), operator.lt),
    (BaseImpact(**impact_config, value=RangeValue(min=1, max=2)), BaseImpact(**impact_config, value=2), operator.le),
    (BaseImpact(**impact_config, value=RangeValue(min=2, max=3)), BaseImpact(**impact_config, value=2), operator.ge),
    (BaseImpact(**impact_config, value=RangeValue(min=2, max=3)), BaseImpact(**impact_config, value=1), operator.gt),
    (BaseImpact(**impact_config, value=RangeValue(min=1, max=2)), BaseImpact(**impact_config, value=1), operator.ne),

    (
            BaseImpact(**impact_config, value=RangeValue(min=1, max=2)),
            BaseImpact(**impact_config, value=RangeValue(min=1, max=2)),
            operator.eq
    ),
    (
            BaseImpact(**impact_config, value=RangeValue(min=1, max=2)),
            BaseImpact(**impact_config, value=RangeValue(min=3, max=4)),
            operator.lt
    ),
    (
            BaseImpact(**impact_config, value=RangeValue(min=1, max=2)),
            BaseImpact(**impact_config, value=RangeValue(min=2, max=3)),
            operator.le
    ),
    (
            BaseImpact(**impact_config, value=RangeValue(min=2, max=3)),
            BaseImpact(**impact_config, value=RangeValue(min=1, max=2)),
            operator.ge
    ),
    (
            BaseImpact(**impact_config, value=RangeValue(min=3, max=4)),
            BaseImpact(**impact_config, value=RangeValue(min=1, max=2)),
            operator.gt
    ),
    (
            BaseImpact(**impact_config, value=RangeValue(min=1, max=2)),
            BaseImpact(**impact_config, value=RangeValue(min=1, max=3)),
            operator.ne
    )
])
def test_impact_compare(impact_1, impact_2, op):
    assert op(impact_1, impact_2)


@pytest.mark.parametrize('impact_1,impact_2,op', [
    (BaseImpact(**impact_config, value=1), BaseImpact(type="other", name="Other", value=1, unit=""), operator.eq),
    (
            BaseImpact(**impact_config, value=RangeValue(min=1, max=2)),
            BaseImpact(type="other", name="Other", value=1, unit=""),
            operator.ge
    ),
    (
            BaseImpact(**impact_config, value=RangeValue(min=1, max=2)),
            BaseImpact(type="other", name="Other", value=RangeValue(min=1, max=2), unit=""),
            operator.le
    ),
    (Energy(value=1), GWP(value=1), operator.gt),
    (Energy(value=1), ADPe(value=1), operator.lt),
    (Energy(value=1), PE(value=1), operator.ne),
    (GWP(value=1), ADPe(value=1), operator.eq),
    (GWP(value=1), PE(value=1), operator.ge),
    (ADPe(value=1), PE(value=1), operator.le),
])
def test_impact_cannot_compare(impact_1, impact_2, op):
    with pytest.raises(ModelingError):
        op(impact_1, impact_2)


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
