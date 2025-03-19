from typing import Union, Tuple, List, Optional
import psycopg as pg


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

    def base_connect_and_change_table(self, query: str, params: Optional[Union[Tuple, str]] = None) -> Optional[List[Tuple]]:
        """
        Executes a given SQL query and optionally fetches results if it is a SELECT query.
        
        Args:
            query (str): The SQL query to execute.
            params (Optional[Union[Tuple, str]]): The parameters for the query, if applicable.

        Returns:
            Optional[List[Tuple]]: The results of the query if it is a SELECT query, otherwise None.
        """
        try:
            with pg.connect(self.connection_details) as connection:
                with connection.cursor() as cursor:
                    if isinstance(params, str):
                        params = (params,)
                    cursor.execute(query, params if params else ())

                    if query.strip().lower().startswith('select'):
                        return cursor.fetchall()
                    connection.commit()
                    return None
        except pg.DatabaseError as e:
            print(f"DatabaseError: {e}")  # Log the error
            raise  # Re-raise the exception for further handling
        except Exception as e:
            print(f"Unexpected error: {e}")  # Log the error
            raise  # Re-raise the exception for further handling

    def base_update(self, table_name: str, columns: Union[tuple, str], values: Union[tuple, str], id_column_name: str, id_value: str):
        """
        Updates a specific record in a table.
        
        Args:
            table_name (str): The name of the table.
            columns (Union[tuple, str]): The columns to update.
            values (Union[tuple, str]): The new values for the columns.
            id_column_name (str): The name of the identifier column.
            id_value (str): The identifier value of the record to update.
        """
        try:
            if isinstance(values, str):
                values = tuple(values)
            if isinstance(columns, str):
                columns = (columns,)

            columns_str = ', '.join([f'{columns[i]} = %s' for i in range(len(columns))])
            query = f'UPDATE {table_name} SET {columns_str} WHERE {id_column_name} = %s;'
            params = values + (id_value,)
            self.base_connect_and_change_table(query, params)
        except Exception as e:
            print(f"Unexpected error in base_update: {e}")
            raise

    def base_add(self, table_name: str, columns: Union[tuple, str], values: Union[tuple, str]):
        """
        Inserts a new record into a table.
        
        Args:
            table_name (str): The name of the table.
            columns (Union[tuple, str]): The columns to insert values into.
            values (Union[tuple, str]): The values to be inserted.
        """
        try:
            if isinstance(values, str):
                values = (values,)
            if isinstance(columns, str):
                columns = (columns,)

            placeholders = ', '.join(['%s'] * len(values))
            query = f'INSERT INTO {table_name}({", ".join(columns)}) VALUES({placeholders});'
            self.base_connect_and_change_table(query, values)
        except pg.DatabaseError as e:
            print(f"IntegrityError: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in base_add: {e}")
            raise

    def base_print_all(self, table_name: str, order: str = None):
        """
        Retrieves all records from a table.
        
        Args:
            table_name (str): The name of the table.

        Returns:
            Optional[List[Tuple]]: A list of tuples representing the table rows.
        """
        try:
            query = f'SELECT * FROM {table_name} {order};'
            return self.base_connect_and_change_table(query)
        except Exception as e:
            print(f"Unexpected error in base_print_all: {e}")
            raise

    def base_delete_by_id(self, table_name: str, id_column_name: str, id_value: str):
        """
        Deletes a record from a table by ID.
        
        Args:
            table_name (str): The name of the table.
            id_column_name (str): The name of the identifier column.
            id_value (str): The identifier value of the record to delete.
        """
        try:
            if isinstance(id_column_name, tuple):
                id_column_names = ""
                for i in range(len(id_column_name)):
                    id_column_names += f'{id_column_name[i]} = %s ' 
                query = f'DELETE FROM {table_name} WHERE {id_column_names};'
            else:
                id_value = (id_value,)
                query = f'DELETE FROM {table_name} WHERE {id_column_name} = %s;'
            self.base_connect_and_change_table(query, id_value)
        except Exception as e:
            print(f"Unexpected error in base_delete_by_id: {e}")
            raise

    def base_print_wanted_column_value_by_id(self, table_name: str, column_name: str, id_column_name: str, id_value: str):
        """
        Retrieves specific column values from a record by ID.
        
        Args:
            table_name (str): The name of the table.
            column_name (str): The column(s) to retrieve values from.
            id_column_name (str): The name of the identifier column.
            id_value (str): The identifier value of the record to fetch data from.
        
        Returns:
            Optional[List[Tuple]]: A list of tuples representing the fetched column values.
        """
        try:
            if isinstance(id_column_name, tuple):
                id_column_names = ""
                for i in range(len(id_column_name)):
                    id_column_names += f'{id_column_name[i]} = %s ' 
                query = f'SELECT {column_name} FROM {table_name} WHERE {id_column_names};'
            else:
                query = f'SELECT {column_name} FROM {table_name} WHERE {id_column_name} = %s;'
            return self.base_connect_and_change_table(query, id_value)
        except Exception as e:
            print(f"Unexpected error in base_print_wanted_column_value_by_id: {e}")
            raise
