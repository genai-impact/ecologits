import pytest
from ecologits.model_repository import ModelRepository, Model


def test_create_model_repository_default():
    models = ModelRepository.from_csv()
    assert isinstance(models, ModelRepository)
    assert models.find_model(provider="openai", model_name="gpt-3.5-turbo") is not None


def test_create_model_repository_from_scratch():
    models = ModelRepository([
        Model(provider="provider-test", name="model-test")
    ])
    assert models.find_model(provider="provider-test", model_name="model-test")

def test_find_azure_openai_model():
    models = ModelRepository.from_csv()
    assert models.find_model(provider="openai", model_name="gpt-35-turbo").name =="gpt-3.5-turbo"


@pytest.mark.parametrize("input_provider,input_name, expected_name",
                         [("openai", "gpt-35-turbo", "gpt-3.5-turbo"),
                          ("openai", "gpt-3.5-turbo", "gpt-3.5-turbo"),
                          ("openai", "gpt-4", "gpt-4"),
                          ("openai", "gpt-4-turbo", "gpt-4-turbo"),
                          ("mistralai", "mistral-small-2312", "mistral-small-2312"),
                          ("mistralai", "mistral-small-notarealversion", "mistral-small"),
                          ("google", "gemini-1.5-flash", "gemini-1.5-flash"),
                         ])
def test_nominal_matching_cases(input_provider, input_name, expected_name):
    models = ModelRepository.from_csv()
    assert models.find_model(provider=input_provider, model_name=input_name).name ==expected_name


def test_find_unknown_provider():
    models = ModelRepository.from_csv()
    assert models.find_model(provider="provider-test", model_name="gpt-3.5-turbo") is None


def test_find_unknown_model_name():
    models = ModelRepository.from_csv()
    assert models.find_model(provider="openai", model_name="model-test") is None


def test_find_huggingface_provider():
    models = ModelRepository.from_csv()
    assert models.find_provider(model_name="huggingface/HuggingFaceH4/zephyr-7b-beta") == "huggingface_hub"
