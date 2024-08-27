import os
from csv import DictReader
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Zones(Enum):
    world = "WOR"
    europe = "EEE"
    zimbabwe = "ZWE"
    zambia = "ZMB"
    south_africa = "ZAF"
    yemen = "YEM"
    vietnam = "VNM"
    venezuela = "VEN"
    uzbekistan = "UZB"
    uruguay = "URY"
    united_states = "USA"
    ukraine = "UKR"
    tanzania = "TZA"
    taiwan = "TWN"
    trinidad_and_tobago = "TTO"
    turkey = "TUR"
    tunisia = "TUN"
    turkmenistan = "TKM"
    tajikistan = "TJK"
    thailand = "THA"
    togo = "TGO"
    syrian_arab_republic = "SYR"
    el_salvador = "SLV"
    senegal = "SEN"
    slovak_republic = "SVK"
    slovenia = "SVN"
    singapore = "SGP"
    sweden = "SWE"
    sudan = "SDN"
    saudi_arabia = "SAU"
    russian_federation = "RUS"
    serbia_and_montenegro = "SCG"
    romania = "ROU"
    qatar = "QAT"
    paraguay = "PRY"
    portugal = "PRT"
    poland = "POL"
    pakistan = "PAK"
    philippines = "PHL"
    peru = "PER"
    panama = "PAN"
    oman = "OMN"
    new_zealand = "NZL"
    nepal = "NPL"
    norway = "NOR"
    netherlands = "NLD"
    nicaragua = "NIC"
    nigeria = "NGA"
    namibia = "NAM"
    mozambique = "MOZ"
    malaysia = "MYS"
    mexico = "MEX"
    malta = "MLT"
    mongolia = "MNG"
    myanmar = "MMR"
    north_macedonia = "MKD"
    moldova = "MDA"
    morocco = "MAR"
    libya = "LBY"
    latvia = "LVA"
    luxembourg = "LUX"
    lithuania = "LTU"
    sri_lanka = "LKA"
    lebanon = "LBN"
    kazakhstan = "KAZ"
    kuwait = "KWT"
    south_korea = "KOR"
    north_korea = "PRK"
    cambodia = "KHM"
    kyrgyz_republic = "KGZ"
    kenya = "KEN"
    japan = "JPN"
    jordan = "JOR"
    jamaica = "JAM"
    italy = "ITA"
    iceland = "ISL"
    iran = "IRN"
    iraq = "IRQ"
    india = "IND"
    israel = "ISR"
    ireland = "IRL"
    indonesia = "IDN"
    hungary = "HUN"
    haiti = "HTI"
    croatia = "HRV"
    honduras = "HND"
    guatemala = "GTM"
    greece = "GRC"
    ghana = "GHA"
    georgia = "GEO"
    united_kingdom = "GBR"
    gabon = "GAB"
    france = "FRA"
    finland = "FIN"
    ethiopia = "ETH"
    spain = "ESP"
    eritrea = "ERI"
    egypt = "EGY"
    estonia = "EST"
    ecuador = "ECU"
    algeria = "DZA"
    dominican_republic = "DOM"
    denmark = "DNK"
    germany = "DEU"
    czech_republic = "CZE"
    cyprus = "CYP"
    cuba = "CUB"
    costa_rica = "CRI"
    colombia = "COL"
    china = "CHN"
    cameroon = "CMR"
    chile = "CHL"
    cote_d_ivoire = "CIV"
    switzerland = "CHE"
    congo = "COG"
    democratic_republic_of_the_congo = "COD"
    canada = "CAN"
    belarus = "BLR"
    botswana = "BWA"
    brazil = "BRA"
    bolivia = "BOL"
    brunei = "BRN"
    benin = "BEN"
    bahrain = "BHR"
    bulgaria = "BGR"
    belgium = "BEL"
    bangladesh = "BGD"
    bosnia_and_herzegovina = "BIH"
    azerbaijan = "AZE"
    australia = "AUS"
    austria = "AUT"
    argentina = "ARG"
    angola = "AGO"
    armenia = "ARM"
    albania = "ALB"
    united_arab_emirates = "ARE"


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
                        zone=Zones(row["name"]).name,
                        adpe=float(row["adpe"]),
                        pe=float(row["pe"]),
                        gwp=float(row["gwp"]),
                    )
                )
        return cls(electricity_mixes)

electricity_mixes = ElectricityMixRepository.from_csv()
