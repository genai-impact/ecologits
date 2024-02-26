from typing import Optional

from openai import OpenAI


class GenAIImpacts:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs
    ):
        self._openai_client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            **kwargs
        )

    def get_impacts(self, response):
        return Impacts(
            energy=42,  # Dummy values, replace with real calculations
            energy_unit='kWh',
            gwp=15,
            gwp_unit='kgCO2eq'
        )

    def __getattr__(self, name):
        """
        Redirect attribute access to the underlying openai client if the attribute
        is not defined in this class.
        """
        return getattr(self._openai_client, name)

class Impacts:
    def __init__(self, energy, energy_unit, gwp, gwp_unit):
        self.energy = energy
        self.energy_unit = energy_unit
        self.gwp = gwp
        self.gwp_unit = gwp_unit

    def __str__(self):
        return f"Impacts(energy={self.energy}, energy_unit='{self.energy_unit}', gwp={self.gwp}, gwp_unit='{self.gwp_unit}')"
