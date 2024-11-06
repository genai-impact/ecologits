class EcoLogitsError(Exception):
    pass


class TracerInitializationError(EcoLogitsError):
    """Tracer is initialized twice"""
    pass


class ModelingError(EcoLogitsError):
    """Operation or computation not allowed"""
    pass
