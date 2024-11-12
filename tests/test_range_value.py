from ecologits.utils.range_value import RangeValue


def test_range_formats_ok():
    
    range = RangeValue(min =0.00000006, max=0.00008)
    
    expected = f"{range.min:.2f} to {range.max:.2f}"

    assert f"{range:.2f}" == expected