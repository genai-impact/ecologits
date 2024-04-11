import pytest
from ecologits import Ecologits
from ecologits.exceptions import EcologitsError


def test_double_init(tracer_init):
    with pytest.raises(EcologitsError) as e:
        Ecologits.init()   # Second initialization
