

from src.bll.user_facade import UserFacade
from src.dal.DAO.users_dao import UsersDAO
from src.config import DB_CONFIG_TESTS


import unittest


import psycopg as pg


def execute_sql_file() -> None:
    """
    Executes the SQL commands in the initialization file to reset the test database.
    """
    with open(r"src\init_test_database.sql", 'r') as file:
        sql_commands = file.read()

    with pg.connect(DB_CONFIG_TESTS) as connection:
        with connection.cursor() as cursor:
            for command in sql_commands.split(";"):
                if command.strip():
                    cursor.execute(command)
            connection.commit()


class UserFacadeTests(unittest.TestCase):
    """
    Test suite for the UserFacade class.
    """

    def setUp(self) -> None:
        """
        Sets up the test environment for each test case by resetting the database and initializing the facade.
        """
        self.user_facade = UserFacade(DB_CONFIG_TESTS)
        self.user_dao = UsersDAO(DB_CONFIG_TESTS)
        execute_sql_file()

    def tearDown(self) -> None:
        """
        Cleans up the test environment after each test case by resetting the database.
        """
        execute_sql_file()

    def test_log_in_success(self) -> None:
        """
        Tests successful login with valid credentials.
        """
        self.user_facade.log_in('asaflotz@gmail.com', '4567889')
        self.assertTrue(self.user_dao.print_user_by_email_and_password('asaflotz@gmail.com', '4567889'))

    def test_log_in_wrong_password(self) -> None:
        """
        Tests login with a wrong password, expecting a ValueError.
        """
        with self.assertRaises(ValueError) as context:
            self.user_facade.log_in('asaflotz@gmail.com', '45678229')
        self.assertEqual("Wrong email or password.", str(context.exception))

    def test_register_user_success(self) -> None:
        """
        Tests successful user registration.
        """
        self.user_facade.register_user('3', 'Jane', 'Smith', 'jane.smith@example.com', 'anotherPassword', '2')

        results = self.user_facade.log_in('jane.smith@example.com', 'anotherPassword')
        results = [(str(r[0]), str(r[1]), r[2], str(r[3]), str(r[4]), int(r[5])) for r in results]

        self.assertEqual(results, [('3', 'Jane', 'Smith', 'jane.smith@example.com', 'anotherPassword', 2)])

    def test_register_invalid_email(self) -> None:
        """
        Tests registering a user with an invalid email format.
        """
        with self.assertRaises(Exception) as context:
            self.user_facade.register_user('3', 'Jane', 'Smith', 'jane.smith@example.c', 'anotherPassword', 2)
        self.assertEqual("Invalid email format", str(context.exception))

    def test_like_vacation_success(self) -> None:
        """
        Tests successfully liking a vacation.
        """
        self.user_facade.like_vacation(1, 10)
        results = self.user_dao.likes_print_wanted_column_value_by_id('1', 10)
        self.assertEqual(results, [(1, 10)])

    def test_like_vacation_not_existing_vacation_id(self) -> None:
        """
        Tests liking a non-existent vacation, expecting a DatabaseError.
        """
        with self.assertRaises(pg.DatabaseError) as context:
            self.user_facade.like_vacation(2, 20)
        self.assertIn('insert or update on table "likes" violates foreign key constraint "likes_vacation_id_fkey"', str(context.exception))

    def test_unlike_success(self) -> None:
        """
        Tests successfully unliking a vacation.
        """
        self.user_facade.like_vacation(1, 10)
        self.user_facade.unlike_vacation(1, 10)
        self.assertFalse(self.user_dao.likes_print_wanted_column_value_by_id(1, 10))

    def test_unlike_wrong_vacation_and_user_id(self) -> None:
        """
        Tests unliking a vacation with mismatched user and vacation IDs, expecting a ValueError.
        """
        self.user_facade.like_vacation(2, 6)
        with self.assertRaises(ValueError) as context:
            self.user_facade.unlike_vacation(2, 5)
        self.assertEqual('Cannot unlike a vacation that was not liked.', str(context.exception))
