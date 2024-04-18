import pytest
from ecologits import EcoLogits
from ecologits.exceptions import EcoLogitsError


@pytest.mark.skip(reason="Double init does not raise an error anymore, but we should test that it works correctly.")
def test_double_init(tracer_init):
    with pytest.raises(EcoLogitsError) as e:
        EcoLogits.init()   # Second initialization
