from ecologits.electricity_mix_repository import ElectricityMix, ElectricityMixRepository


def test_create_electricity_mix_repository_default():
    electricity_mixes = ElectricityMixRepository.from_csv()
    assert isinstance(electricity_mixes, ElectricityMixRepository)
    assert electricity_mixes.find_electricity_mix(zone="BEL") is not None


def test_create_electricity_mix_repository_from_scratch():
    electricity_mixes = ElectricityMixRepository([
        ElectricityMix(
            zone="wonderland",
            adpe=0.,
            pe=0.,
            gwp=0.,
            wcf=0.
        )
    ])
    assert electricity_mixes.find_electricity_mix(zone="wonderland") is not None


def test_find_unknown_zone():
    electricity_mixes = ElectricityMixRepository.from_csv()
    assert electricity_mixes.find_electricity_mix(zone="AAA") is None

