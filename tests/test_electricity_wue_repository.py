from ecologits.repositories.electricity_wue_repository import ElectricityWUERepository, ElectricityWUE


def test_create_electricity_wue_repository_default():
    electricity_wue_list = ElectricityWUERepository.from_csv()
    assert isinstance(electricity_wue_list, ElectricityWUERepository)
    assert electricity_wue_list.find_electricity_wue(zone="BEL") is not None


def test_create_electricity_wue_repository_from_scratch():
    electricity_wue_list = ElectricityWUERepository([
        ElectricityWUE(
            zone="wonderland", 
            wue=0., 
        )
    ])
    assert electricity_wue_list.find_electricity_wue(zone="wonderland") is not None


def test_find_unknown_zone():
    electricity_wue_list = ElectricityWUERepository.from_csv()
    assert electricity_wue_list.find_electricity_wue(zone="AAA") is None

