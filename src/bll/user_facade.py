from dal.DAO import countries_dao, roles_dao, users_dao, vacations_dao, likes_dao
from models import countries_dto, roles_dto, likes_dto, users_dto, vacations_dto
import psycopg as pg
import re


class UserFacade:
    def __init__(self, connection_details):
        self.users_dao = users_dao.UsersDAO(connection_details)

    def check_password_contains_more_than_3(self, password:str):
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters long")
    
    def check_email_valid(self, email:str):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise ValueError("Invalid email format")


    def register_user(self, user_id: str, first_name: str, last_name: str, email: str, password: str, role_id: str):
        if not user_id or not first_name or not last_name or email or not password or not role_id:
            raise ValueError("All fields are required.")
        user_dto = users_dto.UserDTO(user_id, first_name, last_name, email, password, role_id)
        
        self.check_email_valid(email)
        
        self.check_password_contains_more_than_3(user_dto.password)

        if len(user_dto.first_name) == 0 or len(user_dto.last_name) == 0:
            raise ValueError("Both first name and last name cannot be empty.")
        

        if not user_dto.first_name.isalpha() or not user_dto.last_name.isalpha():
            raise ValueError("Both first name and last name can contain alphabet letter only.")
        
        if self.users_dao.check_if_email_exists(user_dto.user_email):
            raise Exception("Cannot register with an email that is already registered.")
        
        columns = ('user_id', 'first_name', 'last_name', 'email', 'password', 'role_id')
        values = (user_dto.user_id, user_dto.first_name, user_dto.last_name, user_dto.user_email, user_dto.password, user_dto.role_id)
        
        self.users_dao.add(columns, values)
    
    def log_in(self, email:str, password:str)-> bool:
        if not email or not password:
            raise ValueError("All fields are required.")
        self.check_password_contains_more_than_3(password)
        self.check_email_valid(email)
        check = self.users_dao.print_user_by_email_and_password(email, password)
        print(check)
        return bool(check)

    def like_vacation(self, user_id, vacation_id):
        like_dto = likes_dto.LikeDTO(user_id, vacation_id)
        self.users_dao.like_vacation(like_dto.user_id, like_dto.vacation_id)

    def unlike_vacation(self, user_id, vacation_id):
        like_dto = likes_dto.LikeDTO(user_id, vacation_id)
        self.users_dao.unlike_vacation(like_dto.user_id, like_dto.vacation_id)






        