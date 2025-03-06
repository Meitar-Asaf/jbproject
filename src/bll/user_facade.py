from dal.DAO import countries_dao, roles_dao, users_dao, vacations_dao
from models import countries_dto, roles_dto, users, likes_dto, vacations_dto
import psycopg as pg
import re


class UserFacade:
    def __init__(self, connection_details):
        self.users_dao = users_dao.UsersDAO(connection_details)

    def register_user(self, user_id: str, first_name: str, last_name: str, email: str, password: str, role_id: str):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise ValueError("Invalid email format")
        
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters long")