from unittest import TestCase

from src.main.states import validate_states_ids


class StatesFromConfValidateTest(TestCase):

    def test_blank(self):
        user_insert = ''
        res = validate_states_ids(user_insert)
        self.assertEqual(res, [], msg='If user states blank, result must be []')

    def test_empty_commas(self):
        user_insert = ',,,,'
        res = validate_states_ids(user_insert)
        self.assertEqual(res, [], )

    def test_one_valid(self):
        user_insert = 'AL'
        res = validate_states_ids(user_insert)
        self.assertEqual(res, ['AL'], )

    def test_one_valid_with_coma(self):
        user_insert = 'AL,'
        res = validate_states_ids(user_insert)
        self.assertEqual(res, ['AL'], )

    def test_one_valid_lower_case(self):
        user_insert = 'al'
        res = validate_states_ids(user_insert)
        self.assertEqual(res, ['AL'], )

    def test_few_valid(self):
        user_insert = 'AL,AK,AZ'
        res = validate_states_ids(user_insert)
        self.assertEqual(res, ['AL', 'AK', 'AZ'], )

    def test_few_valid_with_space(self):
        user_insert = '  AL,  AK,  AZ  '
        res = validate_states_ids(user_insert)
        self.assertEqual(res, ['AL', 'AK', 'AZ'], )

    def test_one_invalid_code(self):
        user_insert = 'XX,'
        with self.assertRaisesRegex(ValueError, 'Incorrect state id XX'):
            validate_states_ids(user_insert)

    def test_few_one_invalid(self):
        user_insert = 'AL,AK,AZ,XX,'
        with self.assertRaisesRegex(ValueError, 'Incorrect state id XX'):
            validate_states_ids(user_insert)