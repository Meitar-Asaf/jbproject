from dal.DAO import countries_dao, roles_dao, users_dao, vacations_dao
from models import countries_dto, roles_dto, users, likes_dto, vacations_dto
import psycopg as pg
import re


class UserFacade:
    def __init__(self, connection_details):
        self.users_dao = users_dao.UsersDAO(connection_details)

    def check_password_contains_more_than_3(self, password):
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters long")


    def register_user(self, user_id: str, first_name: str, last_name: str, email: str, password: str, role_id: str):
        user_dto = users.UserDTO(user_id, first_name, last_name, email, password, role_id)
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", user_dto.user_email):
            raise ValueError("Invalid email format")
        
        self.check_password_contains_more_than_3(user_dto.password)
        

        if not user_dto.first_name.isalpha() or not user_dto.last_name.isalpha():
            raise ValueError("Both first name and last name can contain alphabet letter only.")
        
        if self.users_dao.check_if_email_exists(user_dto.user_email):
            raise Exception("Cannot register with an email that is already registered.")
        
        columns = ('user_id', 'first_name', 'last_name', 'email', 'password', 'role_id')
        values = (user_dto.user_id, user_dto.first_name, user_dto.last_name, user_dto.user_email, user_dto.password, user_dto.role_id)
        
        self.users_dao.add(columns, values)
    
    def log_in(self, email, password):
        if not email or not password:
            raise ValueError("All fields are required.")
        if self.check_password_contains_more_than_3(password)
        if
        