class EcologitsError(Exception):
    pass


class TracerInitializationError(EcologitsError):
    """Tracer is initialized twice"""
    pass
