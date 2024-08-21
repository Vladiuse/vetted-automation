import pytest

from src.main.states import get_states_from_conf


@pytest.mark.parametrize(
    'env_value',
    (
            '',  # empty string
            ',,,,',  # commas
            '   ',  # spaces
            ', , , , , ',  # spaces and commas
    ),
)
def test_empty_result(monkeypatch, env_value):
    monkeypatch.setenv('PREFERRED_TRAVEL_STATE', env_value)
    assert get_states_from_conf() == []


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
def test_one_item_valid(monkeypatch, env_value):
    monkeypatch.setenv('PREFERRED_TRAVEL_STATE', env_value)
    assert get_states_from_conf() == ['AL', ]


@pytest.mark.parametrize(
    'env_value, expected',
    (
            ('AL,AK,', ['AL', 'AK', ]),
            ('AL,AK,AZ', ['AL', 'AK', 'AZ']),
            ('AL, AK,  AZ  ', ['AL', 'AK', 'AZ']),
    ),
)
def test_few_valid(monkeypatch, env_value, expected):
    monkeypatch.setenv('PREFERRED_TRAVEL_STATE', env_value)
    assert get_states_from_conf() == expected


@pytest.mark.parametrize(
    'env_value',
    (
            'xx,',
            'xxx,',
            'XX',
            'AL,AK,AZ,XX,',
    ),
)
def test_invalid(monkeypatch, env_value):
    monkeypatch.setenv('PREFERRED_TRAVEL_STATE', env_value)
    with pytest.raises(ValueError):
        get_states_from_conf()
