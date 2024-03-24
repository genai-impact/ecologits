class GenAIImpactError(Exception):
    pass


class TracerInitializationError(GenAIImpactError):
    """Tracer is initialized twice"""
    pass
