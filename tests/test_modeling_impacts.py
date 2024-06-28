import operator

import pytest

from ecologits.impacts.modeling import Impact, RangeValue, Energy, GWP, ADPe, PE
from ecologits.exceptions import ModelingError


impact_config = dict(
    type="test",
    name="Test",
    unit=""
)


@pytest.mark.parametrize('impact_1,impact_2,result', [
    (
        Impact(**impact_config, value=1),
        Impact(**impact_config, value=1),
        Impact(**impact_config, value=2)
    ),
    (
        Impact(**impact_config, value=RangeValue(min=1, max=2)),
        Impact(**impact_config, value=1),
        Impact(**impact_config, value=RangeValue(min=2, max=3))
    ),
    (
        Impact(**impact_config, value=RangeValue(min=1, max=2)),
        Impact(**impact_config, value=RangeValue(min=1, max=2)),
        Impact(**impact_config, value=RangeValue(min=2, max=4))
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
    (Impact(**impact_config, value=1), Impact(type="other", name="Other", value=1, unit="")),
    (Impact(**impact_config, value=RangeValue(min=1, max=2)), Impact(type="other", name="Other", value=1, unit="")),
    (Impact(**impact_config, value=RangeValue(min=1, max=2)),
     Impact(type="other", name="Other", value=RangeValue(min=1, max=2), unit="")),
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
    (Impact(**impact_config, value=1), Impact(**impact_config, value=1), operator.eq),
    (Impact(**impact_config, value=1), Impact(**impact_config, value=2), operator.lt),
    (Impact(**impact_config, value=2), Impact(**impact_config, value=2), operator.le),
    (Impact(**impact_config, value=2), Impact(**impact_config, value=2), operator.ge),
    (Impact(**impact_config, value=2), Impact(**impact_config, value=1), operator.gt),
    (Impact(**impact_config, value=2), Impact(**impact_config, value=1), operator.ne),

    (Impact(**impact_config, value=RangeValue(min=1, max=1)), Impact(**impact_config, value=1), operator.eq),
    (Impact(**impact_config, value=RangeValue(min=1, max=2)), Impact(**impact_config, value=3), operator.lt),
    (Impact(**impact_config, value=RangeValue(min=1, max=2)), Impact(**impact_config, value=2), operator.le),
    (Impact(**impact_config, value=RangeValue(min=2, max=3)), Impact(**impact_config, value=2), operator.ge),
    (Impact(**impact_config, value=RangeValue(min=2, max=3)), Impact(**impact_config, value=1), operator.gt),
    (Impact(**impact_config, value=RangeValue(min=1, max=2)), Impact(**impact_config, value=1), operator.ne),

    (
        Impact(**impact_config, value=RangeValue(min=1, max=2)),
        Impact(**impact_config, value=RangeValue(min=1, max=2)),
        operator.eq
    ),
    (
        Impact(**impact_config, value=RangeValue(min=1, max=2)),
        Impact(**impact_config, value=RangeValue(min=3, max=4)),
        operator.lt
    ),
    (
        Impact(**impact_config, value=RangeValue(min=1, max=2)),
        Impact(**impact_config, value=RangeValue(min=2, max=3)),
        operator.le
    ),
    (
        Impact(**impact_config, value=RangeValue(min=2, max=3)),
        Impact(**impact_config, value=RangeValue(min=1, max=2)),
        operator.ge
    ),
    (
        Impact(**impact_config, value=RangeValue(min=3, max=4)),
        Impact(**impact_config, value=RangeValue(min=1, max=2)),
        operator.gt
    ),
    (
        Impact(**impact_config, value=RangeValue(min=1, max=2)),
        Impact(**impact_config, value=RangeValue(min=1, max=3)),
        operator.ne
    )
])
def test_impact_compare(impact_1, impact_2, op):
    assert op(impact_1, impact_2)


@pytest.mark.parametrize('impact_1,impact_2,op', [
    (Impact(**impact_config, value=1), Impact(type="other", name="Other", value=1, unit=""), operator.eq),
    (
        Impact(**impact_config, value=RangeValue(min=1, max=2)),
        Impact(type="other", name="Other", value=1, unit=""),
        operator.ge
    ),
    (
        Impact(**impact_config, value=RangeValue(min=1, max=2)),
        Impact(type="other", name="Other", value=RangeValue(min=1, max=2), unit=""),
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
