from typing import Optional

from pydantic import BaseModel


class BaseWarning(BaseModel):
    text: Optional[str] = None

    @classmethod
    def from_code(cls, code: str) -> "BaseWarning":
        if code not in _warning_codes:
            raise ValueError(f"Unknown annotation code: {code}")
        return _warning_codes[code]()


class BaseError(BaseModel):
    text: Optional[str] = None


class ModelArchNotReleasedWarning(BaseWarning):
    text: str = "The model architecture has not been released, expect lower precision."


class ModelArchMultimodalWarning(BaseWarning):
    text: str = "The model architecture is multimodal, expect lower precision."


class ModelNotRegisteredError(BaseError):
    text: str = "The model is not registered in the model repository."


class ZoneDoesNotExistError(BaseError):
    text: str = "The zone does not exist."


_warning_codes: dict[str, type[BaseWarning]] = {
    "model_architecture_not_released": ModelArchNotReleasedWarning,
    "model_architecture_multimodal": ModelArchMultimodalWarning
}
