from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.main.recruiters import RecruiterForm


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




