
import logging
from unittest.mock import Mock, patch

from ecologits._ecologits import _INSTRUMENTS, EcoLogits

default_path = "this_is_patched.toml"
default_providers = providers=list(set(_INSTRUMENTS.keys()))
default_electricity_mix = "WOR"

user_electricity_mix = "FRA"
user_providers_list = list(set(["openai", "mistral"]))
user_single_provider = ["openai"]


@patch("ecologits._ecologits.init_instruments", Mock)
class TestEcoLogitsConfig:

    @patch(target="ecologits._ecologits.EcoLogits._read_ecologits_config", return_value = {"electricity_mix_zone":user_electricity_mix, "providers":user_providers_list})
    def test_working_config_provider_list(self, toml):
        EcoLogits.init(config_path=default_path)

        assert EcoLogits.config.providers == user_providers_list
        assert EcoLogits.config.electricity_mix_zone == user_electricity_mix

    @patch(target="ecologits._ecologits.EcoLogits._read_ecologits_config", return_value = {"electricity_mix_zone":user_electricity_mix, "providers":user_single_provider})
    def test_working_config_single_provider(self, toml):
        EcoLogits.init(config_path=default_path)

        assert EcoLogits.config.providers == user_single_provider
        assert EcoLogits.config.electricity_mix_zone == user_electricity_mix

    def test_non_existing_file(self, caplog):
        with caplog.at_level(logging.WARNING):
            EcoLogits.init(config_path=default_path)

        assert EcoLogits.config.providers == default_providers
        assert EcoLogits.config.electricity_mix_zone == default_electricity_mix
        assert "Provided file does not exist, will fall back on default values" in caplog.text

    @patch(target="ecologits._ecologits.EcoLogits._read_ecologits_config", return_value = {"electricity_mix_zone":user_electricity_mix})
    def test_only_elec_mix_provided(self, patch):

        EcoLogits.init(config_path=default_path)

        assert EcoLogits.config.providers == default_providers
        assert EcoLogits.config.electricity_mix_zone == user_electricity_mix

    @patch(target="ecologits._ecologits.EcoLogits._read_ecologits_config", return_value = {"providers":user_providers_list})
    def test_only_provider_in_config(self, patch):
        EcoLogits.init(config_path=default_path)

        assert EcoLogits.config.providers == user_providers_list
        assert EcoLogits.config.electricity_mix_zone == default_electricity_mix

    def test_no_ecologits_key_in_toml(self, caplog):
        with caplog.at_level(logging.WARNING):
            EcoLogits.init(config_path="./tests/config/toml_with_no_ecologits.toml")

        assert EcoLogits.config.providers == default_providers
        assert EcoLogits.config.electricity_mix_zone == default_electricity_mix
        assert "Provided file did not contain the ecologits key. Falling back on default configuration" in caplog.text

    def test_init_parameters_both_provided(self):
        EcoLogits.init(providers = user_providers_list, electricity_mix_zone=user_electricity_mix)

        assert EcoLogits.config.providers == user_providers_list
        assert EcoLogits.config.electricity_mix_zone == user_electricity_mix

    def test_init_parameters_elec_only_provided(self):
        EcoLogits.init(electricity_mix_zone=user_electricity_mix)

        assert EcoLogits.config.providers == default_providers
        assert EcoLogits.config.electricity_mix_zone == user_electricity_mix

    def test_init_parameters_providers_only_provided(self):
        EcoLogits.init(providers=user_providers_list)

        assert EcoLogits.config.providers == user_providers_list
        assert EcoLogits.config.electricity_mix_zone == default_electricity_mix

    @patch(target="ecologits._ecologits.EcoLogits._read_ecologits_config", return_value = {"providers":user_providers_list})
    def test_init_parameters_and_config_provided(self, patch, caplog):
        EcoLogits.init(config_path=default_path, providers=["anthropic"])

        assert EcoLogits.config.providers == ["anthropic"]
        assert EcoLogits.config.electricity_mix_zone == default_electricity_mix
        assert "Both config path and init arguments provided, init arguments will be prioritized" in caplog.text