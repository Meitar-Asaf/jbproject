


from src.dal.DAO.base_DAO import BaseDAO, Union, Tuple, List, Any, Optional



class UsersDAO(BaseDAO):
    """
    Data Access Object (DAO) class for handling operations related to the 'users' table in the database.

    Attributes:
        connection_details (str): The connection details for the database.
        table_name (str): The name of the 'users' table in the database.
        user_id_column (str): The primary key column name for the users table.
    """

    def __init__(self, connection_details: str):
        """
        Initializes the UsersDAO with the given connection details.

        Args:
            connection_details (str): The connection details for the database.
        """
        self.connection_details = connection_details
        self.table_name = 'users'
        self.user_id_column = 'user_id'

    def update(self, columns: Union[Tuple[str, ...], str], values: Union[Tuple[Any, ...], str], user_id: str):
        """
        Updates a specific user record in the database.

        Args:
            columns (Union[Tuple[str, ...], str]): The columns to update, either as a tuple or a single string.
            values (Union[Tuple[Any, ...], str]): The new values for the columns, either as a tuple or a single value.
            user_id (str): The unique identifier of the user record to update.
        """
        self.base_update(self.table_name, columns, values,
                         self.user_id_column, user_id)

    def add(self, columns: Union[Tuple[str, ...], str], values: Union[Tuple[Any, ...], str]):
        """
        Inserts a new user record into the database, with restrictions for adding admin users.

        Args:
            columns (Union[Tuple[str, ...], str]): The columns for which values will be inserted.
            values (Union[Tuple[Any, ...], str]): The values to insert into the specified columns.

        Raises:
            ValueError: If attempting to insert an admin user ('1') directly through this method.
        """
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

    def print_all(self) -> Optional[List[Tuple[Any, ...]]]:
        """
        Retrieves all user records from the database.

        Returns:
            Optional[List[Tuple[Any, ...]]]: A list of tuples representing the user records.
        """
        return self.base_print_all(self.table_name)

    def delete_by_id(self, user_id: str):
        """
        Deletes a user record from the database by its unique identifier.

        Args:
            user_id (str): The unique identifier of the user record to delete.
        """
        self.base_delete_by_id(self.table_name, self.user_id_column, user_id)

    def print_wanted_column_value_by_id(self, column_name: str, user_id: str) -> Optional[List[Tuple[Any, ...]]]:
        """
        Retrieves specific column values for a user record by its unique identifier.

        Args:
            column_name (str): The name of the column(s) to retrieve.
            user_id (str): The unique identifier of the user record.

        Returns:
            Optional[List[Tuple[Any, ...]]]: A list of tuples representing the fetched column values.
        """
        return self.base_print_wanted_column_value_by_id(
            self.table_name, column_name, self.user_id_column, user_id
        )

    def like_vacation(self, user_id: str, vacation_id: str):
        """
        Adds a 'like' for a specific vacation by a user.

        Args:
            user_id (str): The unique identifier of the user.
            vacation_id (str): The unique identifier of the vacation.
        """
        self.base_add('likes', (self.user_id_column,
                      'vacation_id'), (user_id, vacation_id))

    def unlike_vacation(self, user_id: str, vacation_id: Optional[str]):
        """
        Removes a 'like' for a specific vacation by a user.

        Args:
            user_id (str): The unique identifier of the user.
            vacation_id (Optional[str]): The unique identifier of the vacation, or None to remove all likes for the user.

        Raises:
            ValueError: If attempting to unlike a vacation that was not previously liked.
        """
        if vacation_id is None:
            results = self.base_connect_and_change_table(
                "SELECT * FROM likes WHERE user_id = %s AND vacation_id = %s", (
                    user_id, vacation_id)
            )
            if not results:
                raise ValueError(
                    'Cannot unlike a vacation that was not liked.')
            return self.base_delete_by_id('likes', self.user_id_column, user_id)

        results = self.base_connect_and_change_table(
            "SELECT * FROM likes WHERE user_id = %s AND vacation_id = %s", (
                user_id, vacation_id)
        )
        if not results:
            raise ValueError('Cannot unlike a vacation that was not liked.')
        return self.base_delete_by_id('likes', ('vacation_id', ' AND ' + self.user_id_column), (vacation_id, user_id))

    def print_user_by_email_and_password(self, email: str, password: str) -> Optional[List[Tuple[Any, ...]]]:
        """
        Retrieves a user record by email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            Optional[List[Tuple[Any, ...]]]: A list of tuples representing the user record.
        """
        query = f'SELECT * FROM {self.table_name} WHERE email = %s AND password = %s'
        return self.base_connect_and_change_table(query, (email, password))

    def check_if_email_exists(self, email: str) -> bool:
        """
        Checks if a given email exists in the users table.

        Args:
            email (str): The email to check.

        Returns:
            bool: True if the email exists, False otherwise.
        """
        query = f'SELECT * FROM {self.table_name} WHERE email = %s'
        results = self.base_connect_and_change_table(query, email)
        return bool(results)

    def likes_print_wanted_column_value_by_id(self, user_id: str, vacation_id: str) -> Optional[List[Tuple[Any, ...]]]:
        """
        Retrieves specific 'likes' records for a user and vacation.

        Args:
            user_id (str): The unique identifier of the user.
            vacation_id (str): The unique identifier of the vacation.

        Returns:
            Optional[List[Tuple[Any, ...]]]: A list of tuples representing the 'likes' records.
        """
        return self.base_print_wanted_column_value_by_id(
            'likes', 'user_id, vacation_id', (self.user_id_column,
                                              ' AND vacation_id'), (user_id, vacation_id)
        )
