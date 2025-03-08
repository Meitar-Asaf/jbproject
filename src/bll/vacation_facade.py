from dal.DAO import countries_dao, roles_dao, users_dao, vacations_dao, likes_dao
from models import countries_dto, roles_dto, likes_dto, users_dto, vacations_dto
import psycopg as pg
import re

class VacationFacade:
    def __init__(self, connection_details):
        self.vacation_dao = vacations_dao.VacationsDAO(connection_details)
    
    def delete_vacation(self, vacation_id:str):
        self.vacation_dao.delete_by_id(vacation_id)