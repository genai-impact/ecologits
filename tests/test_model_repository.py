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


def test_find_unknown_provider():
    models = ModelRepository.from_csv()
    assert models.find_model(provider="provider-test", model_name="gpt-3.5-turbo") is None


def test_find_unknown_model_name():
    models = ModelRepository.from_csv()
    assert models.find_model(provider="openai", model_name="model-test") is None

def test_find_huggingface_provider():
    models = ModelRepository.from_csv()
    assert models.find_provider(model_name="huggingface/HuggingFaceH4/zephyr-7b-beta") == "huggingface_hub"
