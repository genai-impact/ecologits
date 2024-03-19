import pytest
from genai_impact import Tracer

def test_double_init(tracer_init):
    with pytest.raises(Exception) as excinfo:  
        Tracer.init() # Second initialization
    assert str(excinfo.value) == "Tracer is already initialized"  