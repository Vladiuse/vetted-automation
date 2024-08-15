from unittest import TestCase
from unittest.mock import patch

from src.main.recruiters import Recruiter, RecruiterForm, Recruiters


class RecruiterFormTest(TestCase):

    def setUp(self):
        self.valid_name = 'Some'
        self.valid_is_active = '0'
        self.valid_init_data = {
            'name': self.valid_name,
            'is_active': self.valid_is_active,
        }

    def test_incorrect_fields_name(self):
        data = {
            '1': '1'
        }

        form = RecruiterForm(data)
        with self.assertRaises(KeyError):
            form.validate()

    def test_name_valid_remove_space(self):
        res = RecruiterForm._validate_name(' Some Some ')
        self.assertEqual(res, 'Some Some')

    def test_is_active_not_int_value(self):
        value = 'x'
        with self.assertRaises(ValueError):
            RecruiterForm._validate_is_active(value)

    def test_is_active_not_valid_int(self):
        value = 10
        with self.assertRaises(ValueError):
            RecruiterForm._validate_is_active(str(value))

    def test_is_active_valid_value(self):
        for value in (0, 1):
            res = RecruiterForm._validate_is_active(str(value))
            self.assertEqual(res, value)
            self.assertIsInstance(res, bool)

    @patch.object(RecruiterForm, '_validate_name')
    def test_validate_name_called(self, mock_validate_name):
        form = RecruiterForm(self.valid_init_data)
        form.validate()
        self.assertTrue(mock_validate_name.called)
        mock_validate_name.assert_called_once_with(self.valid_name)

    @patch.object(RecruiterForm, '_validate_is_active')
    def test_validate_is_valid_called(self, mock_validate_is_active):
        form = RecruiterForm(self.valid_init_data)
        form.validate()
        self.assertTrue(mock_validate_is_active.called)
        mock_validate_is_active.assert_called_once_with(self.valid_is_active)


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
        res = recruiters.get_active_rec_names()
        self.assertListEqual(res, ['Some 1', 'Some 2',])