from pydantic import BaseModel

STATUS_DOCS_URL = "https://ecologits/tutorial/warnings_and_errors/#{code}"


class _StatusMessage(BaseModel):
    """
    Base status message used for warnings or errors.

    Attributes:
        code: Status code.
        message: Message explaining the issue.
    """
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.message} For further information visit {STATUS_DOCS_URL.format(code=self.code)}"

    @classmethod
    def from_code(cls, code: str) -> type["_StatusMessage"]:
        raise NotImplementedError("Should be called from WarningMessage or ErrorMessage.")


class WarningMessage(_StatusMessage):
    """
    Warning message.

    Attributes:
        code: Warning code.
        message: Warning message.
    """

    @classmethod
    def from_code(cls, code: str) -> "WarningMessage":
        if code in _warning_codes:
            return _warning_codes[code]()
        else:
            raise ValueError(f"Warning code `{code}` does not exist.")


class ErrorMessage(_StatusMessage):
    """
    Error message.

    Attributes:
        code: Error code.
        message: Error message.
    """

    @classmethod
    def from_code(cls, code: str) -> "ErrorMessage":
        if code in _error_codes:
            return _error_codes[code]()
        else:
            raise ValueError(f"Error code `{code}` does not exist.")


class ModelArchNotReleasedWarning(WarningMessage):
    code: str = "model-arch-not-released"
    message: str = "The model architecture has not been released, expect lower precision."


class ModelArchMultimodalWarning(WarningMessage):
    code: str = "model-arch-multimodal"
    message: str = "The model architecture is multimodal, expect lower precision."


class ModelNotRegisteredError(ErrorMessage):
    code: str = "model-not-registered"
    message: str = "The model is not registered in the model repository."


class ZoneNotRegisteredError(ErrorMessage):
    code: str = "zone-not-registered"
    message: str = "The zone is not registered."


_warning_codes: dict[str, type[WarningMessage]] = {
    "model-arch-not-released": ModelArchNotReleasedWarning,
    "model-arch-multimodal": ModelArchMultimodalWarning
}

_error_codes: dict[str, type[ErrorMessage]] = {
    "model-not-registered": ModelNotRegisteredError,
    "zone-not-registered": ZoneNotRegisteredError
}
