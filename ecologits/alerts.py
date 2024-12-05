from pydantic import BaseModel

ALERT_DOCS_URL = "https://ecologits/tutorial/alerts/#{code}"


class AlertMessage(BaseModel):
    """
    Base alert message used for warnings or errors.

    Attributes:
        code: Alert code.
        message: Message explaining the alert.
    """
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.message}\n\nFor further information visit {ALERT_DOCS_URL.format(code=self.code)}"

    @classmethod
    def from_code(cls, code: str) -> "AlertMessage":
        if code in _warning_codes:
            return _warning_codes[code]()
        elif code in _error_codes:
            return _error_codes[code]()
        else:
            raise ValueError(f"Alert code `{code}` does not exist.")


class ModelArchNotReleasedWarning(AlertMessage):
    code: str = "model-arch-not-released"
    message: str = "The model architecture has not been released, expect lower precision."


class ModelArchMultimodalWarning(AlertMessage):
    code: str = "model-arch-multimodal"
    message: str = "The model architecture is multimodal, expect lower precision."


class ModelNotRegisteredError(AlertMessage):
    code: str = "model-not-registered"
    message: str = "The model is not registered in the model repository."


class ZoneNotRegisteredError(AlertMessage):
    code: str = "zone-not-registered"
    message: str = "The zone is not registered."


_warning_codes: dict[str, type[AlertMessage]] = {
    "model-arch-not-released": ModelArchNotReleasedWarning,
    "model-arch-multimodal": ModelArchMultimodalWarning
}

_error_codes: dict[str, type[AlertMessage]] = {
    "model-not-registered": ModelNotRegisteredError,
    "zone-not-registered": ZoneNotRegisteredError
}
