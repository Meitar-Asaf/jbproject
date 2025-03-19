from src.bll.vacation_facade import VacationFacade
from src.dal.DAO.vacations_dao import VacationsDAO
from src.config import DB_CONFIG_TESTS
import unittest
import psycopg as pg


def execute_sql_file():
    with open(r"src\init_test_database.sql", 'r') as file:
        sql_commands = file.read()

    with pg.connect(DB_CONFIG_TESTS) as connection:
        with connection.cursor() as cursor:
            for command in sql_commands.split(";"):
                if command.strip():
                    cursor.execute(command)
            connection.commit()


class VacationFacadeTests(unittest.TestCase):
    def setUp(self):
        self.vacation_facade = VacationFacade(DB_CONFIG_TESTS)
        self.vacations_dao = VacationsDAO(DB_CONFIG_TESTS)
        execute_sql_file()
    def tearDown(self):
        execute_sql_file()
    # Positive test case
    def test_add_vacation_success(self):
        args_tuple = (
            "13",
            "1",
            "Relaxing vacation in Israel",
            "2025-05-01",
            "2025-05-10",
            2500,
            "israel.jpg"
        )
        self.vacation_facade.add_vacation(
            "13",
            "1",
            "Relaxing vacation in Israel",
            "2025-05-01",
            "2025-05-10",
            2500,
            "israel.jpg"
        )
        results = self.vacations_dao.print_wanted_column_value_by_id('*', '13')
        results = [(str(r[0]), str(r[1]), r[2], str(r[3]),
                    str(r[4]), int(r[5]), r[6]) for r in results]
        self.assertEqual([args_tuple], results)

    # Negative test cases
    def test_add_vacation_missing_fields(self):
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.add_vacation(
                vacation_id=None,
                country_id="1",
                vacation_description="Relaxing vacation in Israel",
                beginning_date="2025-05-01",
                end_date="2025-05-10",
                price=2500,
                picture_file_name="israel.jpg"
            )
        self.assertEqual(str(context.exception), "All fields are required.")

    def test_add_vacation_invalid_date_format(self):
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.add_vacation(
                "14",
                "1",
                "Relaxing vacation in Israel",
                "2025-13-01",  # Invalid month
                "2025-05-10",
                2500,
                "israel.jpg"
            )
        self.assertEqual(
            str(context.exception),
            "Invalid date format: 2025-13-01. Please use 'YYYY-MM-DD'."
        )

    def test_add_vacation_negative_price(self):
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.add_vacation(
                "14",
                "1",
                "Relaxing vacation in Israel",
                "2025-05-01",
                "2025-05-10",
                -100,  # Negative price
                "israel.jpg"
            )
        self.assertEqual(str(context.exception),
                         "Vacation cannot be priced 0 or lower.")

    def test_add_vacation_price_too_high(self):
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.add_vacation(
                "14",
                "1",
                "Relaxing vacation in Israel",
                "2025-05-01",
                "2025-05-10",
                15000,  # Price exceeds maximum allowed
                "israel.jpg"
            )
        self.assertEqual(str(context.exception),
                         "Vacation cannot be priced higher than 10,000")

    def test_add_vacation_missing_picture(self):
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.add_vacation(
                "14",
                "1",
                "Relaxing vacation in Israel",
                "2025-05-01",
                "2025-05-10",
                2500,
                picture_file_name=None  # Missing picture filename
            )
        self.assertEqual(str(context.exception), "All fields are required.")

    def test_add_vacation_end_date_before_start_date(self):
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.add_vacation(
                "14",
                "1",
                "Relaxing vacation in Israel",
                "2025-05-10",
                "2025-05-01",  # End date is before start date
                2500,
                "israel.jpg"
            )
        self.assertEqual(str(context.exception),
                         "Vacation end date cannot be earlier than the beginning date.")

    def test_add_vacation_start_date_in_past(self):
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.add_vacation(
                "14",
                "1",
                "Relaxing vacation in Israel",
                "2022-05-01",  # Start date is in the past
                "2025-05-10",
                2500,
                "israel.jpg"
            )
        self.assertEqual(str(context.exception),
                         "Vacation beginning date cannot be earlier than today.")

    def test_add_vacation_duplicate_id(self):
        # Insert the first vacation
        self.vacation_facade.add_vacation(
            "13", "1", "Relaxing vacation in Israel", "2025-05-01", "2025-05-10", 2500, "israel.jpg"
        )

    # Attempt to insert a duplicate vacation, expect UniqueViolation
        with self.assertRaises(Exception) as context:
            self.vacation_facade.add_vacation(
                "13", "1", "Another vacation", "2025-06-01", "2025-06-10", 3000, "another.jpg"
            )

    # Optional: Check the exception message
        self.assertIn(
            "duplicate key value violates unique constraint", str(context.exception))

    def test_delete_vacation_success(self):
        self.vacation_facade.delete_vacation("1")
        results = self.vacations_dao.print_wanted_column_value_by_id('*', '1')
        self.assertEqual([], results)

    def test_delete_vacation_id_doesnt_exist(self):
        with self.assertRaises(Exception) as context:
            self.vacation_facade.delete_vacation("100")
        self.assertIn("does not exist", str(context.exception))

    def test_update_success(self):
        self.vacation_facade.update_vacation('6', '6', 'Vacation in Sydney with stunning opera houses and beautiful beaches', '2025-11-20', '2025-11-29', 3800, 'sydney.jpg')
        results = self.vacations_dao.print_wanted_column_value_by_id('*', '6')
        results = [(str(r[0]), str(r[1]), r[2], str(r[3]),
                    str(r[4]), int(r[5]), r[6]) for r in results]
        self.assertEqual([('6', '6', 'Vacation in Sydney with stunning opera houses and beautiful beaches', '2025-11-20', '2025-11-29', 3800, 'sydney.jpg')], results)

    def test_update_success_without_image(self):
        self.vacation_facade.update_vacation('7', '6', 'Vacation in Sydney with stunning opera houses and beautiful beaches', '2025-11-20', '2025-11-29', 3800)
        results = self.vacations_dao.print_wanted_column_value_by_id('*', '7')
        results = [(str(r[0]), str(r[1]), r[2], str(r[3]),
                    str(r[4]), int(r[5])) for r in results]
        self.assertEqual([('7', '6', 'Vacation in Sydney with stunning opera houses and beautiful beaches', '2025-11-20', '2025-11-29', 3800)], results)

    def test_update_no_price(self):
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.update_vacation('12', '6', 'Vacation in Melbourne with artistic culture and great coffee', '2026-02-15', '2026-02-22', None, 'melbourne.jpg')
        self.assertEqual("All fields are required.", str(context.exception))
    
    def test_print_all_vacations_by_date(self):
        results_1 = self.vacation_facade.print_all_vacation_ordered_by_beginning_date()
        results_2 = self.vacations_dao.print_all('ORDER BY beginning_date')
        self.assertEqual(results_1, results_2)