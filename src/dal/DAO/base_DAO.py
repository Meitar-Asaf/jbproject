from src import config
from src.dal.DAO.base_DAO import BaseDAO
from typing import Union, Tuple, List
import psycopg as pg
from psycopg import sql


class BaseDAO:
    def __init__(self, connection_details: str):
        self.connection_details = connection_details

    def connect_and_change_table(self, query: str, params: Union[tuple,str]):
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
            
                        
        except pg.DatabaseError as e:
            print("Database error: {}".format(e))
        except Exception as e:
            print("Unexpected error: {}".format(e))

    def base_update(self, table_name: str, columns: Union[tuple,str], values: Union[tuple,str], id_column_name: str, id: str):
        if len(columns) != len(values):
            raise ValueError("Number of columns and values must match")


        columns = ', '.join(
            [f'{columns[i]} = %s' for i in range(len(columns))])

    
        query = 'UPDATE ' + table_name + 'SET ' + columns + ' WHERE ' + id_column_name + ' = %s;'
        params = values + id
        self.connect_and_change_table(query, params)

    def base_add(self, table_name:str, columns:Union[tuple,str], values:Union[tuple,str]):
        place_holders = '%s ,' * (len(values) - 1) + '%s'
        query = f'INSERT INTO {table_name}({', '.join(columns)}) VALUES({place_holders});'
        self.connect_and_change_table(query, values)

    def base_print_all(self, table_name:str):
        query = f'SELECT * FROM {table_name};'
        self.connect_and_change_table(query, )

    def base_delete_by_id(self, table_name:str, id_column_name:str, id:str):
        query = f'DELETE FROM {table_name} WHERE {id_column_name} = %s'
        self.connect_and_change_table(query, id)

    def base_print_wanted_column_value_by_id(self, table_name:str, column_name:str,id_column_name:str, id:str):
        query = f'SELECT {column_name} FROM {table_name} WHERE {id_column_name} = %s'
        self.connect_and_change_table(query, id)
