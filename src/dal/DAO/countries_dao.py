


from src.dal.DAO.base_DAO import BaseDAO, Union, Tuple, List, Any, Optional




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

    def update(self, columns: Union[Tuple[str, ...], str], values: Union[Tuple[Any, ...], str], country_id: str):
        """
        Updates a specific country record in the database.

        Args:
            columns (Union[Tuple[str, ...], str]): The columns to update, either as a tuple or a single string.
            values (Union[Tuple[Any, ...], str]): The new values for the columns, either as a tuple or a single value.
            country_id (str): The unique identifier of the country record to update.
        """
        self.base_update(self.table_name, columns, values,
                         self.id_column, country_id)

    def add(self, columns: Union[Tuple[str, ...], str], values: Union[Tuple[Any, ...], str]):
        """
        Inserts a new country record into the database.

        Args:
            columns (Union[Tuple[str, ...], str]): The columns for which values will be inserted, as a tuple or single string.
            values (Union[Tuple[Any, ...], str]): The values to insert into the specified columns, as a tuple or single value.
        """
        self.base_add(self.table_name, columns, values)

    def print_all(self):
        """
        Retrieves all country records from the database.

        Returns:
            Optional[List[Tuple[Any, ...]]]: A list of tuples representing the country records.
        """
        self.base_print_all(self.table_name)

    def delete_by_id(self, country_id: str):
        """
        Deletes a country record from the database by its unique identifier.

        Args:
            country_id (str): The unique identifier of the country record to delete.
        """
        self.base_delete_by_id(self.table_name, self.id_column, country_id)

    def print_wanted_column_value_by_id(self, column_name: str, country_id: str) -> Optional[List[Tuple[Any, ...]]]:
        """
        Retrieves specific column values for a country record by its unique identifier.

        Args:
            column_name (str): The name of the column(s) to retrieve.
            country_id (str): The unique identifier of the country record.

        Returns:
            Optional[List[Tuple[Any, ...]]]: A list of tuples representing the fetched column values.
        """
        return self.base_print_wanted_column_value_by_id(self.table_name, column_name, self.id_column, country_id)
