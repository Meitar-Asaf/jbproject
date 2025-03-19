from src.dal.DAO.base_DAO import BaseDAO, Union, Tuple, List


class VacationsDAO(BaseDAO):
    """
    Data Access Object (DAO) class for handling vacation-related database operations.
    
    Attributes:
        connection_details (str): The connection details for the database.
        table_name (str): The name of the table in the database.
        id_column (str): The primary key column name for the vacations table.
    """
    
    def __init__(self, connection_details: str):
        """
        Initializes the VacationsDAO with the given connection details.

        Args:
            connection_details (str): The connection details for the database.
        """
        self.connection_details = connection_details
        self.table_name = 'vacations'
        self.id_column = 'vacation_id'

    def update(self, columns: Union[tuple, str], values: Union[tuple, str], vacation_id: str):
        """
        Updates a specific vacation record in the database.
        
        Args:
            columns (Union[tuple, str]): The columns to update.
            values (Union[tuple, str]): The new values for the columns.
            vacation_id (str): The unique identifier of the vacation record to update.
        """
        self.base_update(self.table_name, columns, values,
                         self.id_column, vacation_id)

    def add(self, columns: Union[tuple, str], values: Union[tuple, str]):
        """
        Inserts a new vacation record into the database.
        
        Args:
            columns (Union[tuple, str]): The columns for which values will be inserted.
            values (Union[tuple, str]): The values to insert into the specified columns.
        """
        self.base_add(self.table_name, columns, values)

    def print_all(self, order:str = None):
        """
        Retrieves all vacation records from the database.
        
        Returns:
            Optional[List[Tuple]]: A list of tuples representing the vacation records.
        """
        return self.base_print_all(self.table_name, order)

    def delete_by_id(self, vacation_id: str):
        """
        Deletes a vacation record from the database by its unique identifier.
        
        Args:
            vacation_id (str): The unique identifier of the vacation record to delete.
        """
        self.base_delete_by_id(self.table_name, self.id_column, vacation_id)

    def print_wanted_column_value_by_id(self, column_name: str, vacation_id: str):
        """
        Retrieves specific column values for a vacation record by its unique identifier.
        
        Args:
            column_name (str): The name of the column(s) to retrieve.
            vacation_id (str): The unique identifier of the vacation record.
        
        Returns:
            Optional[List[Tuple]]: A list of tuples representing the fetched column values.
        """
        return self.base_print_wanted_column_value_by_id(
            self.table_name, column_name, self.id_column, vacation_id)
