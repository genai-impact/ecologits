import pytest
from genai_impact import Tracer
from genai_impact.exceptions import GenAIImpactError

def test_double_init(tracer_init):
    with pytest.raises(GenAIImpactError) as e:  
        Tracer.init() # Second initialization
