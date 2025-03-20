from src.dal.DAO import users_dao
from src.models import likes_dto, users_dto

import re


import psycopg as pg



class UserFacade:
    """
    A facade class providing user-related functionality, such as registration, login, and vacation interactions.

    Attributes:
        users_dao (UsersDAO): Data Access Object (DAO) for user-related database operations.
    """

    def __init__(self, connection_details: str):
        """
        Initializes the UserFacade with the given database connection details.

        Args:
            connection_details (str): The connection details for the database.
        """
        self.users_dao = users_dao.UsersDAO(connection_details)

    def check_password_contains_more_than_3(self, password: str):
        """
        Ensures the password contains at least 4 characters.

        Args:
            password (str): The password to check.

        Raises:
            ValueError: If the password is shorter than 4 characters.
        """
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters long")
    
    def check_email_valid(self, email: str):
        """
        Validates the email format.

        Args:
            email (str): The email to validate.

        Raises:
            ValueError: If the email format is invalid.
        """
        if not re.match(r"^(?!\.)[a-zA-Z0-9._%+-]{1,64}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise ValueError("Invalid email format")

    def register_user(self, user_id: str = None, first_name: str = None, last_name: str = None, email: str = None, password: str = None, role_id: str = None):
        """
        Registers a new user with the provided details.

        Args:
            user_id (str): The unique identifier for the user.
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            email (str): The user's email address.
            password (str): The user's password.
            role_id (str): The role ID for the user.

        Raises:
            ValueError: If any field is missing or invalid.
            Exception: If the email is already registered.
        """
        if not user_id or not first_name or not last_name or not email or not password or not role_id:
            raise ValueError("All fields are required.")

        user_dto = users_dto.UserDTO(user_id, first_name, last_name, email, password, role_id)

        self.check_email_valid(email)
        self.check_password_contains_more_than_3(user_dto.password)

        if len(user_dto.first_name) == 0 or len(user_dto.last_name) == 0:
            raise ValueError("Both first name and last name cannot be empty.")

        if not user_dto.first_name.isalpha() or not user_dto.last_name.isalpha():
            raise ValueError("Both first name and last name can contain alphabet letters only.")

        if self.users_dao.check_if_email_exists(user_dto.user_email):
            raise Exception("Cannot register with an email that is already registered.")

        columns = ('user_id', 'first_name', 'last_name', 'email', 'password', 'role_id')
        values = (user_dto.user_id, user_dto.first_name, user_dto.last_name, user_dto.user_email, user_dto.password, user_dto.role_id)

        self.users_dao.add(columns, values)
    
    def log_in(self, email: str = None, password: str = None) -> bool:
        """
        Logs in a user by validating email and password.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if login is successful, False otherwise.

        Raises:
            ValueError: If email or password is missing or invalid, or if login fails.
        """
        if not email or not password:
            raise ValueError("All fields are required.")

        self.check_password_contains_more_than_3(password)
        self.check_email_valid(email)

        email_exists = self.users_dao.check_if_email_exists(email)
        if email_exists:
            check = self.users_dao.print_user_by_email_and_password(email, password)
            if check == []:
                raise ValueError("Wrong email or password.")
            return check
        return email_exists

    def like_vacation(self, user_id: str = None, vacation_id: str = None):
        """
        Likes a vacation on behalf of a user.

        Args:
            user_id (str): The unique identifier of the user.
            vacation_id (str): The unique identifier of the vacation.
        """
        like_dto = likes_dto.LikeDTO(user_id, vacation_id)
        self.users_dao.like_vacation(like_dto.user_id, like_dto.vacation_id)

    def unlike_vacation(self, user_id: str = None, vacation_id: str = None):
        """
        Removes a 'like' for a specific vacation by a user.

        Args:
            user_id (str): The unique identifier of the user.
            vacation_id (str): The unique identifier of the vacation.
        """
        return self.users_dao.unlike_vacation(user_id, vacation_id)







        