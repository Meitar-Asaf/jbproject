from src.dal.DAO.base_DAO import BaseDAO
import psycopg as pg


class RolesDAO(BaseDAO):
    def update(self, columns: tuple, values: tuple, role_id:str):
        super().base_update('roles', columns, values,'role_id', role_id)
    def add(self, columns:tuple, values:tuple):
        super().base_add('roles',columns, values)
    def print_all(self):
        super().base_print_all('roles')
    def

