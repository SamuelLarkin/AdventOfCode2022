from solution import (
        decimal2snafu,
        snafu2dedimal,
        )

import pytest



@pytest.mark.parametrize(
        "snafu,decimal",
        (
            ("1=-0-2", 1747),
            ("12111", 906),
            ("2=0=", 198),
            ("21", 11),
            ("2=01", 201),
            ("111", 31),
            ("20012", 1257),
            ("112", 32),
            ("1=-1=", 353),
            ("1-12", 107),
            ("12", 7),
            ("1=", 3),
            ("122", 37),
            )
        )
def test_snafu2dedimal(snafu: str, decimal: int):
    """
    """
    assert snafu2dedimal(snafu) == decimal



@pytest.mark.parametrize(
        "decimal,snafu",
        (
            (1, "1"),
            (2, "2"),
            (3, "1="),
            (4, "1-"),
            (5, "10"),
            (6, "11"),
            (7, "12"),
            (8, "2="),
            (9, "2-"),
            (10, "20"),
            (15, "1=0"),
            (20, "1-0"),
            (2022, "1=11-2"),
            (12345, "1-0---0"),
            (314159265, "1121-1110-1=0"),
            )
        )
def test_decimal2snafu(decimal: int, snafu: str):
    """
    """
    assert decimal2snafu(decimal) == snafu
