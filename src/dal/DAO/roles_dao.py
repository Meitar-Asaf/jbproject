from src.dal.DAO.base_DAO import BaseDAO, Union, Tuple, List
import psycopg as pg


class RolesDAO(BaseDAO):
    def __init__(self, connection_details: str):
        self.connection_details = connection_details
        self.table_name = 'roles'
        self.id_column = 'role_id'

    def update(self, columns: Union[tuple, str], values: Union[tuple, str], vacation_id: str):
        self.base_update(self.table_name, columns, values,
                         self.id_column, vacation_id)

    def add(self, columns: Union[tuple, str], values: Union[tuple, str]):
        self.base_add(self.table_name, columns, values)

    def print_all(self):
        self.base_print_all(self.table_name)

    def delete_by_id(self, vacation_id: str):
        self.base_delete_by_id(self.table_name, self.id_column, vacation_id)

    def print_wanted_column_value_by_id(self, column_name: str, vacation_id: str):
        self.base_print_wanted_column_value_by_id(
            self.table_name, column_name, self.id_column, vacation_id)
