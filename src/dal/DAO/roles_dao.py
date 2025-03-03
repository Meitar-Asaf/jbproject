from src.dal.DAO.base_DAO import BaseDAO
import psycopg as pg


class RolesDAO(BaseDAO):
    def update(self, columns: tuple, values: tuple, role_id:str):
        super().base_update('roles', columns, values,'role_id', role_id)
    def add(self, columns:tuple, values:tuple):
        super().base_add('roles',columns, values)
    def print_all(self):
        super().base_print_all('roles')
    def delete_by_id(self,id:str):
        super().base_delete_by_id('roles', 'role_id',id)
    def print_wanted_column_value_by_id(self,column_name:str, id:str):
        super().base_print_wanted_column_value_by_id('roles', column_name, 'role_id', id)


