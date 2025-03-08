from src import config
from src.dal.DAO.base_DAO import BaseDAO
from typing import Union, Tuple, List
import psycopg as pg
from psycopg import sql


from typing import Union, Tuple, List
import psycopg as pg
from psycopg import sql


class BaseDAO:
    """
    A base Data Access Object (DAO) class providing common database operations.

    Attributes:
        connection_details (str): Details for connecting to the database.
    """

    def __init__(self, connection_details: str):
        """
        Initialize the BaseDAO with the given connection details.

        Args:
            connection_details (str): The connection details for the database.
        """
        self.connection_details = connection_details

    def base_connect_and_change_table(self, query: str, params: Union[tuple, str]):
        """
        Execute a query to modify the table data and handle the connection.

        Args:
            query (str): The SQL query to be executed.
            params (Union[tuple, str]): The parameters to be used in the SQL query.
        """
        try:
            with pg.connect(self.connection_details) as connection:
                with connection.cursor() as cursor:
                    if params:
                        cursor.execute(query, params if params else ())
                    connection.commit()
                    if query.startswith('SELECT'):
                        results = cursor.fetchall()
                        for result in results:
                            print(result)
                        return results
        except pg.DatabaseError as e:
            print("Database error: {}".format(e))
        except Exception as e:
            print("Unexpected error: {}".format(e))

    def base_update(self, table_name: str, columns: Union[tuple, str], values: Union[tuple, str], id_column_name: str, id_value: str):
        """
        Update records in the specified table.

        Args:
            table_name (str): The name of the table.
            columns (Union[tuple,str]): The columns to be updated.
            values (Union[tuple,str]): The values to be set.
            id_column_name (str): The name of the ID column.
            id_value (str): The value of the ID for the row to be updated.
        """
        try:
            if not isinstance(columns, (tuple, str)):
                raise TypeError("columns must be a tuple or a string")
            if not isinstance(values, (tuple, str)):
                raise TypeError("values must be a tuple or a string")
            if not isinstance(id_column_name, str):
                raise TypeError("id_column_name must be a string")
            if not isinstance(id_value, str):
                raise TypeError("id_value must be a string")

            if len(columns) != len(values):
                raise ValueError("Number of columns and values must match")

            columns = ', '.join(
                [f'{columns[i]} = %s' for i in range(len(columns))])
            query = f'UPDATE {table_name} SET {columns} WHERE {id_column_name} = %s;'
            params = values + (id_value,)
            self.base_connect_and_change_table(query, params)
        except TypeError as e:
            print(f"TypeError: {e}")
        except ValueError as e:
            print(f"ValueError: {e}")
        except Exception as e:
            print(f"Unexpected error in base_update: {e}")

    def base_add(self, table_name: str, columns: Union[tuple, str], values: Union[tuple, str]):
        """
        Add a new record to the specified table.

        Args:
            table_name (str): The name of the table.
            columns (Union[tuple,str]): The columns to be set.
            values (Union[tuple,str]): The values to be inserted.
        """
        try:
            if not isinstance(columns, (tuple, str)):
                raise TypeError("columns must be a tuple or a string")
            if not isinstance(values, (tuple, str)):
                raise TypeError("values must be a tuple or a string")

            placeholders = '%s, ' * (len(values) - 1) + '%s'
            query = f'INSERT INTO {table_name}({", ".join(columns)}) VALUES({placeholders});'
            self.base_connect_and_change_table(query, values)
        except TypeError as e:
            print(f"TypeError: {e}")
        except Exception as e:
            print(f"Unexpected error in base_add: {e}")

    def base_print_all(self, table_name: str):
        """
        Print all records from the specified table.

        Args:
            table_name (str): The name of the table.
        """
        try:
            if not isinstance(table_name, str):
                raise TypeError("table_name must be a string")

            query = f'SELECT * FROM {table_name};'
            self.base_connect_and_change_table(query, None)
        except TypeError as e:
            print(f"TypeError: {e}")
        except Exception as e:
            print(f"Unexpected error in base_print_all: {e}")

    def base_delete_by_id(self, table_name: str, id_column_name: Union[tuple, str], id_value: Union[tuple, str]):
        """
        Delete a record from the specified table by ID.

        Args:
            table_name (str): The name of the table.
            id_column_name (Union[tuple, str]): The name of the ID column.
            id_value (Union[tuple, str]): The value of the ID for the row to be deleted.
        """
        try:
            if isinstance(id_column_name, tuple):
                if not isinstance(id_value, tuple):
                    raise TypeError(
                        'id_column_name and id_value must be both tuples or both strings.')
                condition = ' AND '.join(
                    [f'{col} = %s' for col in id_column_name])
            else:
                if not isinstance(id_value, str):
                    raise TypeError(
                        'id_column_name and id_value must be both tuples or both strings.')
                condition = f'{id_column_name} = %s'

            query = f'DELETE FROM {table_name} WHERE {condition};'
            self.base_connect_and_change_table(query, id_value)
        except TypeError as e:
            print(f"TypeError: {e}")
        except Exception as e:
            print(f"Unexpected error in base_delete_by_id: {e}")

    def base_print_wanted_column_value_by_id(self, table_name: str, column_name: str, id_column_name: str, id_value: str):
        """
        Print the value of a specific column from the specified table by ID.

        Args:
            table_name (str): The name of the table.
            column_name (str): The name of the column to be printed.
            id_column_name (str): The name of the ID column.
            id_value (str): The value of the ID for the row to be queried.
        """
        try:
            if not isinstance(table_name, str):
                raise TypeError("table_name must be a string")
            if not isinstance(column_name, str):
                raise TypeError("column_name must be a string")
            if not isinstance(id_column_name, str):
                raise TypeError("id_column_name must be a string")
            if not isinstance(id_value, str):
                raise TypeError("id_value must be a string")

            query = f'SELECT {column_name} FROM {table_name} WHERE {id_column_name} = %s;'
            self.base_connect_and_change_table(query, id_value)
        except TypeError as e:
            print(f"TypeError: {e}")
        except Exception as e:
            print(
                f"Unexpected error in base_print_wanted_column_value_by_id: {e}")
