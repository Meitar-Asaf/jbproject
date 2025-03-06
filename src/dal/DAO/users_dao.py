from src.dal.DAO.base_DAO import BaseDAO, Union, Tuple, List
import psycopg as pg


class UsersDAO(BaseDAO):
    def __init__(self, connection_details: str):
        self.connection_details = connection_details
        self.table_name = 'users'
        self.id_column = 'user_id'

    def update(self, columns: Union[tuple, str], values: Union[tuple, str], vacation_id: str):
        self.base_update(self.table_name, columns, values,
                         self.id_column, vacation_id)

    def add(self, columns: Union[tuple, str], values: Union[tuple, str]):
        try:
            if isinstance(values, tuple):
                if values[len(values) - 1] == '1':
                    raise ValueError(
                        'admins can only be added through the database itself')
            if values == '1':
                raise ValueError(
                    'admins can only be added through the database itself')
            self.base_add(self.table_name, columns, values)
        except Exception as e:
            print(e)

    def print_all(self):
        self.base_print_all(self.table_name)

    def delete_by_id(self, vacation_id: str):
        self.base_delete_by_id(self.table_name, self.id_column, vacation_id)

    def print_wanted_column_value_by_id(self, column_name: str, vacation_id: str):
        self.base_print_wanted_column_value_by_id(
            self.table_name, column_name, self.id_column, vacation_id)

    def like_vacation(self, user_id, vacation_id: str):
        self.base_add('likes', (self.id_column, 'vacation_id'),
                      (user_id, vacation_id))

    def unlike_vacation(self, user_id, vacation_id: str):
        self.base_delete_by_id(
            'likes', ('vacation_id', self.id_column), (vacation_id, user_id))

    def print_user_by_email_and_password(self, email, password):
        query = f'SELECT * FROM {self.table_name} WHERE email = %s AND password = %s'
        self.base_connect_and_change_table(query, (email, password))

    def check_if_email_exists(self, email:str):
        query = f'SELECT * FROM {self.table_name} WHERE  email = %s'
        results = self.base_connect_and_change_table(query,email)
        if results:
            return True
        else:
            return False