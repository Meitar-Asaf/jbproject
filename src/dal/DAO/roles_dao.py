from src.dal.DAO.base_DAO import BaseDAO
import psycopg as pg


class RolesDAO(BaseDAO):
    def update(self, columns: tuple, values: tuple, role_id:str):
        condition = 'role_id = '
        BaseDAO.base_update('roles', columns, values,condition, role_id)

