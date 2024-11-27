import os
from csv import DictReader
from dataclasses import dataclass
from typing import Optional

WOR_ELECTRICITY_WUE = 3.908036

@dataclass
class ElectricityWUE:
    zone: str
    wue: float


class ElectricityWUERepository:
    def __init__(self, electricity_wue_list: list[ElectricityWUE]) -> None:
        self.__electricity_wue_list = electricity_wue_list

    def add_electricity_wue(self, zone: str, wue: float) -> None:
        electricity_wue_list.append(
                ElectricityWUE(
                    zone=zone,
                    wue=wue,
                )
            )

    def find_electricity_wue(self, zone: str) -> Optional[ElectricityWUE]:
        for electricity_wue in self.__electricity_wue_list:
            if electricity_wue.zone == zone:
                return electricity_wue
        return None

    @classmethod
    def from_csv(cls, filepath: Optional[str] = None) -> "ElectricityWUERepository":
        if filepath is None:
            filepath = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "data", "electricity_wue_list.csv"
            )
        electricity_wue_list = []
        with open(filepath) as fd:
            csv = DictReader(fd)
            for row in csv:
                electricity_wue_list.append(
                    ElectricityWUE(
                        zone=row["name"],
                        wue=float(row["wue"]),
                    )
                )
        return cls(electricity_wue_list)


electricity_wue_list = ElectricityWUERepository.from_csv()
electricity_wue_list.add_electricity_wue(
    zone = "WOR", 
    wue = WOR_ELECTRICITY_WUE
)
