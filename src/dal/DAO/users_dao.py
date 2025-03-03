from src.dal.DAO.base_DAO import BaseDAO
import psycopg as pg


class UsersDAO(BaseDAO):
    def update(self, columns: tuple, values: tuple, role_id:str):
        super().base_update('users', columns, values,'user_id', role_id)
    def add(self, columns:tuple, values:tuple):
        if values[len(values) -1] == 1:
            raise ValueError("Can't add admin user, please try again")
        super().base_add('users',columns, values)
    def print_all(self):
        super().base_print_all('users')
    def delete_by_id(self,id:str):
        super().base_delete_by_id('users', 'user_id',id)
    def print_wanted_column_value_by_id(self,column_name:str, id:str):
        super().base_print_wanted_column_value_by_id('users', column_name, 'user_id', id)
    def like_vacation(self,id, vacation_id:str):
        super().base_add('vacations', ('user_id', 'vacation_id'), (id, vacation_id))
    def unlike_vacation(self, vacation_id:str):
        super().base_delete_by_id('vacations', 'vacation_id', vacation_id)
