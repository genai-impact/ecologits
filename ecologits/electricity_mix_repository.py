import os
from csv import DictReader
from dataclasses import dataclass
from typing import Optional


@dataclass
class ElectricityMix:
    zone: str
    adpe: float
    pe: float
    gwp: float


class ElectricityMixRepository:
    def __init__(self, electricity_mixes: list[ElectricityMix]) -> None:
        self.__electricity_mixes = electricity_mixes

    def find_electricity_mix(self, zone: str) -> Optional[ElectricityMix]:
        for electricity_mix in self.__electricity_mixes:
            if electricity_mix.zone == zone:
                return electricity_mix
        return None

    @classmethod
    def from_csv(cls, filepath: Optional[str] = None) -> "ElectricityMixRepository":
        if filepath is None:
            filepath = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "data", "electricity_mixes.csv"
            )
        electricity_mixes = []
        with open(filepath) as fd:
            csv = DictReader(fd)
            for row in csv:
                electricity_mixes.append(
                    ElectricityMix(
                        zone=row["name"],
                        adpe=float(row["adpe"]),
                        pe=float(row["pe"]),
                        gwp=float(row["gwp"]),
                    )
                )
        return cls(electricity_mixes)

electricity_mixes = ElectricityMixRepository.from_csv()
