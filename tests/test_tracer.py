import pytest
from ecologits import EcoLogits
from ecologits.exceptions import EcoLogitsError


def test_double_init(tracer_init):
    with pytest.raises(EcoLogitsError) as e:
        EcoLogits.init()   # Second initialization
