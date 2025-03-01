from src import config
import psycopg as pg
from psycopg import sql


class BaseDAO:
    def __init__(self, connection_details: str):
        self.connection_details = connection_details

    def connect_and_change_table(self, query: str, params: tuple):
        try:
            with pg.connect(self.connection_details) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    connection.commit()
        except pg.DatabaseError as e:
            print("Database error: {}".format(e))
        except Exception as e:
            print("Unexpected error: {}".format(e))

    def base_update(self, table_name: str, columns: tuple, values: tuple, condition: str, id: str):
        if len(columns) != len(values):
            raise ValueError("Number of columns and values must match")

        # Creating the SET clause dynamically
        columns = ', '.join(
            [f"{columns[i]} = %s" for i in range(len(columns))])

        # Constructing the full SQL query
        query = 'UPDATE ' + table_name + 'SET ' + columns + ' WHERE ' + condition
        params = values + id
        self.connect_and_change_table(query, params)

    def base_add(self, table_name, )
