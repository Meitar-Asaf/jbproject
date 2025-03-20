

from src.bll.vacation_facade import VacationFacade
from src.dal.DAO.vacations_dao import VacationsDAO
from src.config import DB_CONFIG_TESTS


import unittest


import psycopg as pg


def execute_sql_file() -> None:
    """
    Executes SQL commands from the initialization file to reset the test database.
    This ensures a clean database state before each test case.
    """
    with open(r"src\init_test_database.sql", 'r') as file:
        sql_commands = file.read()
    with pg.connect(DB_CONFIG_TESTS) as connection:
        with connection.cursor() as cursor:
            for command in sql_commands.split(";"):
                if command.strip():
                    cursor.execute(command)
            connection.commit()


class VacationFacadeTests(unittest.TestCase):
    """
    Test suite for the VacationFacade class, covering scenarios for adding, updating, 
    and deleting vacation records.
    """

    def setUp(self) -> None:
        """
        Prepares the test environment before each test.
        This includes resetting the database and initializing the VacationFacade and VacationsDAO instances.
        """
        self.vacation_facade = VacationFacade(DB_CONFIG_TESTS)
        self.vacations_dao = VacationsDAO(DB_CONFIG_TESTS)
        execute_sql_file()

    def tearDown(self) -> None:
        """
        Cleans up the test environment after each test.
        This is done by resetting the test database.
        """
        execute_sql_file()

    def test_add_vacation_success(self) -> None:
        """
        Tests successfully adding a new vacation to the database.
        Validates that the vacation is correctly inserted and matches the expected values.
        """
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
        results = [(str(r[0]), str(r[1]), r[2], str(r[3]), str(r[4]), int(r[5]), r[6]) for r in results]
        self.assertEqual([args_tuple], results)

    def test_add_vacation_missing_fields(self) -> None:
        """
        Tests adding a vacation with missing fields, expecting a ValueError.
        """
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

    def test_add_vacation_invalid_date_format(self) -> None:
        """
        Tests adding a vacation with an invalid date format, expecting a ValueError.
        """
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.add_vacation(
                "14",
                "1",
                "Relaxing vacation in Israel",
                "2025-13-01",
                "2025-05-10",
                2500,
                "israel.jpg"
            )
        self.assertEqual(str(context.exception), "Invalid date format: 2025-13-01. Please use 'YYYY-MM-DD'.")

    def test_add_vacation_negative_price(self) -> None:
        """
        Tests adding a vacation with a negative price, expecting a ValueError.
        """
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.add_vacation(
                "14",
                "1",
                "Relaxing vacation in Israel",
                "2025-05-01",
                "2025-05-10",
                -100,
                "israel.jpg"
            )
        self.assertEqual(str(context.exception), "Vacation cannot be priced 0 or lower.")

    def test_add_vacation_price_too_high(self) -> None:
        """
        Tests adding a vacation with a price exceeding the maximum allowed limit, expecting a ValueError.
        """
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.add_vacation(
                "14",
                "1",
                "Relaxing vacation in Israel",
                "2025-05-01",
                "2025-05-10",
                15000,
                "israel.jpg"
            )
        self.assertEqual(str(context.exception), "Vacation cannot be priced higher than 10,000")

    def test_add_vacation_missing_picture(self) -> None:
        """
        Tests adding a vacation with a missing picture file name, expecting a ValueError.
        """
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.add_vacation(
                "14",
                "1",
                "Relaxing vacation in Israel",
                "2025-05-01",
                "2025-05-10",
                2500,
                picture_file_name=None
            )
        self.assertEqual(str(context.exception), "All fields are required.")

    def test_add_vacation_end_date_before_start_date(self) -> None:
        """
        Tests adding a vacation with the end date earlier than the start date, expecting a ValueError.
        """
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.add_vacation(
                "14",
                "1",
                "Relaxing vacation in Israel",
                "2025-05-10",
                "2025-05-01",
                2500,
                "israel.jpg"
            )
        self.assertEqual(str(context.exception), "Vacation end date cannot be earlier than the beginning date.")

    def test_add_vacation_start_date_in_past(self) -> None:
        """
        Tests adding a vacation with a start date in the past, expecting a ValueError.
        """
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.add_vacation(
                "14",
                "1",
                "Relaxing vacation in Israel",
                "2022-05-01",
                "2025-05-10",
                2500,
                "israel.jpg"
            )
        self.assertEqual(str(context.exception), "Vacation beginning date cannot be earlier than today.")

    def test_add_vacation_duplicate_id(self) -> None:
        """
        Tests adding a vacation with a duplicate ID, expecting an exception.
        """
        self.vacation_facade.add_vacation("13", "1", "Relaxing vacation in Israel", "2025-05-01", "2025-05-10", 2500, "israel.jpg")
        with self.assertRaises(Exception) as context:
            self.vacation_facade.add_vacation("13", "1", "Another vacation", "2025-06-01", "2025-06-10", 3000, "another.jpg")
        self.assertIn("duplicate key value violates unique constraint", str(context.exception))

    def test_delete_vacation_success(self) -> None:
        """
        Tests successfully deleting a vacation record by ID.
        """
        self.vacation_facade.delete_vacation("1")
        results = self.vacations_dao.print_wanted_column_value_by_id('*', '1')
        self.assertEqual([], results)

    def test_delete_vacation_id_doesnt_exist(self) -> None:
        """
        Tests deleting a vacation with a non-existent ID, expecting an exception.
        """
        with self.assertRaises(Exception) as context:
            self.vacation_facade.delete_vacation("100")
        self.assertIn("does not exist", str(context.exception))

    def test_update_success(self) -> None:
        """
        Tests successfully updating a vacation record, including its image.
        """
        self.vacation_facade.update_vacation('6', '6', 'Vacation in Sydney with stunning opera houses and beautiful beaches', '2025-11-20', '2025-11-29', 3800, 'sydney.jpg')
        results = self.vacations_dao.print_wanted_column_value_by_id('*', '6')
        results = [(str(r[0]), str(r[1]), r[2], str(r[3]), str(r[4]), int(r[5]), r[6]) for r in results]
        self.assertEqual([('6', '6', 'Vacation in Sydney with stunning opera houses and beautiful beaches', '2025-11-20', '2025-11-29', 3800, 'sydney.jpg')], results)

    def test_update_success_without_image(self) -> None:
        """
        Tests successfully updating a vacation record without modifying its image.
        """
        self.vacation_facade.update_vacation('7', '6', 'Vacation in Sydney with stunning opera houses and beautiful beaches', '2025-11-20', '2025-11-29', 3800)
        results = self.vacations_dao.print_wanted_column_value_by_id('*', '7')
        results = [(str(r[0]), str(r[1]), r[2], str(r[3]),
                    str(r[4]), int(r[5])) for r in results]
        self.assertEqual([('7', '6', 'Vacation in Sydney with stunning opera houses and beautiful beaches', '2025-11-20', '2025-11-29', 3800)], results)

    def test_update_no_price(self):
        """
        Tests updating a vacation without a price, expecting ValueError.
        """
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.update_vacation('12', '6', 'Vacation in Melbourne with artistic culture and great coffee', '2026-02-15', '2026-02-22', None, 'melbourne.jpg')
        self.assertEqual("All fields are required.", str(context.exception))
    
    def test_print_all_vacations_by_date(self):
        """
        Tests successfully printing all vacations ordered by beginning date.
        """
        results_1 = self.vacation_facade.print_all_vacation_ordered_by_beginning_date()
        results_2 = self.vacations_dao.print_all('ORDER BY beginning_date')
        self.assertEqual(results_1, results_2)