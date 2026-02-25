import pytest

from src.main.states import validate_states_ids


@pytest.mark.parametrize(
    'env_value',
    (
            '',
            ',,,,',
            '   ',
            ', , , , , ',
    ),
)
def test_empty_result(env_value: str):
    assert validate_states_ids(env_value) == []


@pytest.mark.parametrize(
    'env_value',
    (
            'AL',
            'AL,',
            'al',
            ',AL',
            ',AL,',
    ),
)
def test_one_item_valid(env_value: str):
    assert validate_states_ids(env_value) == ['AL', ]


@pytest.mark.parametrize(
    'env_value, expected',
    (
            ('AL,AK,', ['AL', 'AK', ],),
            ('AL,AK,AZ', ['AL', 'AK', 'AZ', ],),
            ('AL, AK,  AZ  ', ['AL', 'AK', 'AZ', ],),
    ),
)
def test_few_valid(env_value: str, expected: list[str]):
    assert validate_states_ids(env_value) == expected


@pytest.mark.parametrize(
    'env_value',
    (
            'xx,',
            'xxx,',
            'XX',
            'AL,AK,AZ,XX,',
    ),
)
def test_invalid(env_value: str):
    with pytest.raises(ValueError):
        validate_states_ids(env_value)
