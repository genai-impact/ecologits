from ecologits.mix_repository import MixRepository, Mix


def test_create_mix_repository_default():
    mixes = MixRepository.from_csv()
    assert isinstance(mixes, MixRepository)
    assert mixes.find_mix(zone="belgium") is not None


def test_create_mix_repository_from_scratch():
    mixes = MixRepository([
        Mix(
            zone="wonderland", 
            adpe=0., 
            pe=0.,
            gwp=0.,
        )
    ])
    assert mixes.find_mix(zone="wonderland") is not None


def test_find_unknown_zone():
    mixes = MixRepository.from_csv()
    assert mixes.find_mix(zone="wonderland") is None

