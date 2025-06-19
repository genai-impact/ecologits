from ecologits.model_repository import ModelRepository

def test_create_empty_repository():
    models = ModelRepository()
    assert isinstance(models, ModelRepository)
    assert not models.list_models()


def test_create_model_repository_default():
    models = ModelRepository.from_json()
    assert isinstance(models, ModelRepository)
    assert models.find_model(provider="openai", model_name="gpt-3.5-turbo") is not None


def test_find_unknown_provider():
    models = ModelRepository.from_json()
    assert models.find_model(provider="provider-test", model_name="gpt-3.5-turbo") is None


def test_find_unknown_model_name():
    models = ModelRepository.from_json()
    assert models.find_model(provider="openai", model_name="model-test") is None


def test_ambiguous_names():
    models = ModelRepository.from_json()
    assert models.find_model(provider="openai", model_name="gpt-4").name == "gpt-4"
    assert models.find_model(provider="openai", model_name="gpt-4-turbo").name == "gpt-4-turbo"
    assert models.find_model(provider="openai", model_name="gpt-4o").name == "gpt-4o"
    assert models.find_model(provider="openai", model_name="gpt-35-turbo").name == "gpt-35-turbo"


def test_add_custom_model():
    models = ModelRepository()
    custom_model_data = {
        "provider": "openai",
        "name": "gpt-4.1-2025-04-14",
        "architecture": {
            "type": "moe", 
            "parameters": 1000
        }
    }
    models.add_model(custom_model_data)
    assert models.find_model("openai", "gpt-4.1-2025-04-14") is not None    
