from solution import Range

import pytest


@pytest.mark.parametrize(
        "r1,r2,answer",
        (
            (Range(-3, 13), Range(15, 17), [Range(-3, 13), Range(15,17)]),
            (Range(-3, 14), Range(15, 17), [Range(-3, 17)]),
            (Range(-3, 15), Range(15, 17), [Range(-3, 17)]),
            (Range(-3, 16), Range(15, 17), [Range(-3, 17)]),

            (Range(15, 17), Range(-3, 13), [Range(-3, 13), Range(15,17)]),
            (Range(15, 17), Range(-3, 14), [Range(-3, 17)]),
            (Range(15, 17), Range(-3, 15), [Range(-3, 17)]),
            (Range(15, 17), Range(-3, 16), [Range(-3, 17)]),
            )
        )
def test_range(r1, r2, answer):
    """
    """
    assert r1.merge(r2) == answer
