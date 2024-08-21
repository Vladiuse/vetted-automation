from unittest import TestCase
from unittest.mock import patch

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


class TestRecruiterForm:

    @pytest.mark.parametrize(
        'data',
        (
                {},
                {'1': '1'},
                {'name': '', },
                {'is_active': '', },
        ),
    )
    def test_incorrect_fields_name(self, data):
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
    def test_name_validate(self, value, form):
        assert form._validate_name(value) == 'Some Some'

    @pytest.mark.parametrize(
        'value',
        ('X', 'xx', '10', '2', '-1', '+',),
    )
    def test_invalid_is_active(self, value, form):
        with pytest.raises(ValueError):
            form._validate_is_active(value)

    @pytest.mark.parametrize(
        'value,expected',
        (
                ('0', False,),
                ('1', True,),
        ),
    )
    def test_valid_is_active(self, value, expected, form):
        assert form._validate_is_active(value) == expected

    def test_validate_func(self, form):
        form.validate()
        assert form.data['name'] == 'Some Name'
        assert form.data['is_active'] is True

    def test_create_without_validate(self, form):
        with pytest.raises(AttributeError):
            form.create()

    def test_create_return_class_instance(self, form):
        form.validate()
        recruiter = form.create()
        assert isinstance(recruiter, Recruiter)



class RecruitersTest(TestCase):

    def setUp(self):
        self.recruiter = Recruiter(
            name='Some',
            is_active=True,
        )

    def test_add_recruiter(self):
        recruiters = Recruiters()
        recruiters.add(self.recruiter)
        self.assertEqual(len(recruiters), 1)
        self.assertEqual(self.recruiter, recruiters._recruiters[0])

    @patch.object(Recruiters, '_validate')
    def test_run_validate_when_add(self, mock_validate):
        recruiters = Recruiters()
        recruiters.add(self.recruiter)
        self.assertTrue(mock_validate.called)

    def test_unique_validate_no_doubles(self):
        rec_1 = Recruiter(
            name='Some 1',
            is_active=True,
        )
        rec_2 = Recruiter(
            name='Some 2',
            is_active=True,
        )
        recruiters = Recruiters()
        try:
            recruiters.add(rec_1)
            recruiters.add(rec_2)
        except ValueError:
            self.fail('Value error must not raises, no duplicates')

    def test_unique_validate_no_doubles_exist(self):
        rec_1 = Recruiter(
            name='Some 1',
            is_active=True,
        )
        rec_2 = Recruiter(
            name='Some 1',
            is_active=True,
        )
        recruiters = Recruiters()
        recruiters.add(rec_1)
        with self.assertRaisesRegex(ValueError, 'The name Some 1 is duplicated in file'):
            recruiters.add(rec_2)

    @patch.object(Recruiters, '_validate_all_names_unique')
    def test_validate_call_all_checkers(self, mock_validate_all_names_unique):
        recruiters = Recruiters()
        recruiters._validate()
        self.assertTrue(mock_validate_all_names_unique.called)

    def test_get_active(self):
        rec_1 = Recruiter(
            name='Some 1',
            is_active=True,
        )
        rec_2 = Recruiter(
            name='Some 2',
            is_active=True,
        )
        rec_3 = Recruiter(
            name='Some 3',
            is_active=False,
        )
        recruiters = Recruiters()
        recruiters.add(rec_1)
        recruiters.add(rec_2)
        recruiters.add(rec_3)
        self.assertEqual(len(recruiters), 3)
        active_recs = recruiters._get_active()
        self.assertEqual(len(active_recs), 2)
        self.assertListEqual(active_recs, [rec_1, rec_2])

    def test_get_active_names(self):
        rec_1 = Recruiter(
            name='Some 1',
            is_active=True,
        )
        rec_2 = Recruiter(
            name='Some 2',
            is_active=True,
        )
        rec_3 = Recruiter(
            name='Some 3',
            is_active=False,
        )
        recruiters = Recruiters()
        recruiters.add(rec_1)
        recruiters.add(rec_2)
        recruiters.add(rec_3)
        res = recruiters.get_active_rec_names()
        self.assertEqual(len(recruiters), 3)
        self.assertListEqual(res, ['Some 1', 'Some 2', ])

    def test_raise_if_no_active_recs(self):
        rec_1 = Recruiter(
            name='Some 1',
            is_active=False,
        )
        rec_2 = Recruiter(
            name='Some 2',
            is_active=False,
        )
        recruiters = Recruiters()
        recruiters.add(rec_1)
        recruiters.add(rec_2)
        with self.assertRaisesRegex(ValueError, 'At least one recruiter must be active'):
            recruiters.get_active_rec_names()
