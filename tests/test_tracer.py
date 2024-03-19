import pytest
from genai_impact import Tracer, TracerInitializationError

def test_double_init(tracer_init):
    with pytest.raises(TracerInitializationError) as e:  
        Tracer.init() # Second initialization
