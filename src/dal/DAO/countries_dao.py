# Internal imports
from src.dal.DAO.base_DAO import BaseDAO, Union, Tuple, List

# External imports
import psycopg as pg


class CountriesDAO(BaseDAO):
    """
    Data Access Object (DAO) class for handling operations related to the 'countries' table in the database.

    Attributes:
        connection_details (str): The connection details for the database.
        table_name (str): The name of the table in the database.
        id_column (str): The primary key column name for the countries table.
    """

    def __init__(self, connection_details: str):
        """
        Initializes the CountriesDAO with the given connection details.

        Args:
            connection_details (str): The connection details for the database.
        """
        self.connection_details = connection_details
        self.table_name = 'countries'
        self.id_column = 'country_id'

    def update(self, columns: Union[tuple, str], values: Union[tuple, str], vacation_id: str):
        """
        Updates a specific country record in the database.

        Args:
            columns (Union[tuple, str]): The columns to update.
            values (Union[tuple, str]): The new values for the columns.
            vacation_id (str): The unique identifier of the country record to update.
        """
        self.base_update(self.table_name, columns, values, self.id_column, vacation_id)

    def add(self, columns: Union[tuple, str], values: Union[tuple, str]):
        """
        Inserts a new country record into the database.

        Args:
            columns (Union[tuple, str]): The columns for which values will be inserted.
            values (Union[tuple, str]): The values to insert into the specified columns.
        """
        self.base_add(self.table_name, columns, values)

    def print_all(self):
        """
        Prints all country records from the database.
        """
        self.base_print_all(self.table_name)

    def delete_by_id(self, vacation_id: str):
        """
        Deletes a country record from the database by its unique identifier.

        Args:
            vacation_id (str): The unique identifier of the country record to delete.
        """
        self.base_delete_by_id(self.table_name, self.id_column, vacation_id)

    def print_wanted_column_value_by_id(self, column_name: str, vacation_id: str):
        """
        Retrieves specific column values for a country record by its unique identifier.

        Args:
            column_name (str): The name of the column(s) to retrieve.
            vacation_id (str): The unique identifier of the country record.

        Returns:
            Optional[List[Tuple]]: A list of tuples representing the fetched column values.
        """
        self.base_print_wanted_column_value_by_id(self.table_name, column_name, self.id_column, vacation_id)
