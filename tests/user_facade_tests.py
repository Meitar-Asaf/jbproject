from src.bll.user_facade import UserFacade
from src.dal.DAO.users_dao import UsersDAO
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


class UserFacadeTests(unittest.TestCase):
    def setUp(self):
        self.user_facade = UserFacade(DB_CONFIG_TESTS)
        self.user_dao = UsersDAO(DB_CONFIG_TESTS)
        execute_sql_file()

    def tearDown(self):
        execute_sql_file()

    def test_log_in_success(self):
        self.user_facade.log_in('asaflotz@gmail.com','4567889')
        self.assertTrue(self.user_dao.print_user_by_email_and_password('asaflotz@gmail.com','4567889'))
    def test_log_in_wrong_password(self):
        with self.assertRaises(ValueError) as context:
            self.user_facade.log_in('asaflotz@gmail.com','45678229')
        self.assertEqual("Wrong email or password.", str(context.exception))

    def test_register_user_success(self):

        self.user_facade.register_user('3', 'Jane', 'Smith','jane.smith@example.com', 'anotherPassword','2')

        results = self.user_facade.log_in('jane.smith@example.com', 'anotherPassword')
        results = [(str(r[0]), str(r[1]), r[2], str(r[3]),
                    str(r[4]), int(r[5])) for r in results]

        self.assertEqual(results, [('3', 'Jane', 'Smith','jane.smith@example.com', 'anotherPassword',2)])

    def test_register_invalid_email(self):
        with self.assertRaises(Exception) as context:
            self.user_facade.register_user('3', 'Jane', 'Smith','jane.smith@example.c', 'anotherPassword',2)
        self.assertEqual("Invalid email format", str(context.exception))

    def test_like_vacation_success(self):
        self.user_facade.like_vacation(1, 10)
        results = self.user_dao.likes_print_wanted_column_value_by_id('1', 10)
        self.assertEqual(results,[(1, 10)])


    def test_like_vacation_not_existing_vacation_id(self):
        with self.assertRaises(pg.DatabaseError) as context:
            self.user_facade.like_vacation(2, 20)
        self.assertIn('insert or update on table "likes" violates foreign key constraint "likes_vacation_id_fkey"', str(context.exception))

    def test_unlike_success(self):
        self.user_facade.like_vacation(1, 10)
        self.user_facade.unlike_vacation(1, 10)
        self.assertFalse(self.user_dao.likes_print_wanted_column_value_by_id(1, 10))

    def test_unlike_wrong_vacation_and_user_id(self):
        self.user_facade.like_vacation(2, 6)
        with self.assertRaises(ValueError) as context:
            self.user_facade.unlike_vacation(2, 5)
        self.assertEqual('Cannot unlike a vacation that was not liked.', str(context.exception))

