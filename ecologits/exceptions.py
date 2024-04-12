class EcoLogitsError(Exception):
    pass


class TracerInitializationError(EcoLogitsError):
    """Tracer is initialized twice"""
    pass
