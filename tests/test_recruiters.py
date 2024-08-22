import pytest

from src.main.recruiters import Recruiter, RecruiterForm, Recruiters


@pytest.fixture
def valid_data():
    return {
        'name': ' Some Name ',
        'is_active': '1',
    }


@pytest.fixture
def form(valid_data):
    return RecruiterForm(valid_data)


@pytest.fixture
def active_recruiter_1():
    return Recruiter(
        name='Some One',
        is_active=True,
    )


@pytest.fixture
def active_recruiter_2():
    return Recruiter(
        name='Some Two',
        is_active=True,
    )


@pytest.fixture
def inactive_recruiter():
    return Recruiter(
        name='Some Three',
        is_active=False,
    )


@pytest.fixture
def active_recruiters_names():
    return ['Some One', 'Some Two', ]


@pytest.fixture
def active_recruiters(active_recruiter_1, active_recruiter_2):
    return [active_recruiter_1, active_recruiter_2, ]


@pytest.fixture
def all_recruiters(active_recruiter_1, active_recruiter_2, inactive_recruiter):
    return [active_recruiter_1, active_recruiter_2, inactive_recruiter, ]


@pytest.fixture
def recruiters():
    return Recruiters()


@pytest.fixture
def recruiters_add_items(recruiters, all_recruiters):
    for recruiter in all_recruiters:
        recruiters.add(recruiter)


class TestRecruiterForm:

    @pytest.mark.parametrize(
        'data',
        (
                {},
                {'1': '1',},
                {'name': '', },
                {'is_active': '', },
        ),
    )
    def test_incorrect_fields_name(self, data: dict):
        form = RecruiterForm(data)


        with pytest.raises(KeyError):
            form.validate()

    @pytest.mark.parametrize(
        'value',
        (
                ' Some Some ',
                ' Some Some',
                'Some Some ',
        ),
    )
    def test_name_validate(self, value: str, form: RecruiterForm):
        assert form._validate_name(value) == 'Some Some'

    @pytest.mark.parametrize(
        'value',
        ('X', 'xx', '10', '2', '-1', '+',),
    )
    def test_invalid_is_active(self, value: str, form: RecruiterForm):
        with pytest.raises(ValueError):
            form._validate_is_active(value)

    @pytest.mark.parametrize(
        'value,expected',
        (
                ('0', False,),
                ('1', True,),
        ),
    )
    def test_valid_is_active(self, value: str, expected: bool, form: RecruiterForm):
        assert form._validate_is_active(value) == expected

    def test_validate_func(self, form: RecruiterForm):
        form.validate()


        assert form.data['name'] == 'Some Name'
        assert form.data['is_active'] is True

    def test_create_without_validate(self, form: RecruiterForm):
        with pytest.raises(AttributeError):
            form.create()

    def test_create_return_class_instance(self, form: RecruiterForm):
        form.validate()
        recruiter = form.create()


        assert isinstance(recruiter, Recruiter)


class TestRecruiters:

    def test_add_recruiter(self, recruiters: Recruiters, active_recruiter_1: Recruiter):
        recruiters.add(active_recruiter_1)


        assert len(recruiters) == 1
        assert active_recruiter_1 is recruiters._recruiters[0]

    def test_unique_validate_no_doubles(self, recruiters: Recruiters, all_recruiters: list[Recruiter]):
        try:
            for recruiter in all_recruiters:
                recruiters.add(recruiter)
        except:
            pytest.fail('Unexpected raise')

    def test_unique_validate_double_exist(
            self,
            recruiters: Recruiters,
            recruiters_add_items: None,
            active_recruiter_1: Recruiter,
    ):
        with pytest.raises(ValueError, match='is duplicated in file'):
            recruiters.add(active_recruiter_1)

    def test_get_active_recruiters(
            self,
            recruiters: Recruiters,
            recruiters_add_items: None,
            active_recruiters: list[Recruiter],
    ):
        assert recruiters._get_active() == active_recruiters

    def test_get_all_active_recruiters_names(
            self,
            recruiters: Recruiters,
            recruiters_add_items: None,
            active_recruiters_names: list,
    ):
        assert active_recruiters_names == recruiters.get_active_rec_names()

    def test_raise_if_no_active_recruiters(self, recruiters: Recruiters, inactive_recruiter: Recruiter):
        with pytest.raises(ValueError, match='At least one recruiter must be active'):
            recruiters.get_active_rec_names()
        recruiters.add(inactive_recruiter)
        with pytest.raises(ValueError, match='At least one recruiter must be active'):
            recruiters.get_active_rec_names()
