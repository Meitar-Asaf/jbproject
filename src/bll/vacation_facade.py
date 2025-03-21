from src.dal.DAO import vacations_dao
from src.models import vacations_dto
import datetime


class VacationFacade:
    """
    A facade class providing vacation-related functionality, such as adding, updating, and deleting vacation records.

    Attributes:
        vacation_dao (VacationsDAO): Data Access Object (DAO) for vacation-related database operations.
    """

    def __init__(self, connection_details: str):
        """
        Initializes the VacationFacade with connection details.

        Args:
            connection_details (str): The details required to connect to the database.
        """
        self.vacation_dao = vacations_dao.VacationsDAO(connection_details)

    def delete_vacation(self, vacation_id: str) -> None:
        """
        Deletes a vacation record by its ID.

        Args:
            vacation_id (str): The ID of the vacation to be deleted.

        Raises:
            ValueError: If the vacation with the given ID does not exist.
        """
        if not self.vacation_dao.print_wanted_column_value_by_id('*', vacation_id):
            raise ValueError(f"Vacation with ID {vacation_id} does not exist.")
        self.vacation_dao.delete_by_id(vacation_id)

    def print_all_vacation_ordered_by_beginning_date(self) -> None:
        """
        Prints all vacation records ordered by the beginning date.
        """
        return self.vacation_dao.print_all('ORDER BY beginning_date')

    def _is_valid_date_format(self, date_str: str) -> datetime.date:
        """
        Validates the date format to ensure it matches 'YYYY-MM-DD'.

        Args:
            date_str (str): The date string to validate.

        Returns:
            datetime.date: A datetime object if the date format is valid.

        Raises:
            ValueError: If the date format is invalid.
        """
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(
                f"Invalid date format: {date_str}. Please use 'YYYY-MM-DD'.")

    def _compare_dates(self, beginning_date: str, end_date: str) -> tuple[datetime.date, datetime.date]:
        """
        Compares the beginning and end dates to ensure they are valid.

        Args:
            beginning_date (str): The beginning date as a string.
            end_date (str): The end date as a string.

        Returns:
            tuple[datetime.date, datetime.date]: A tuple of (begin_date_obj, end_date_obj).

        Raises:
            ValueError: If the end date is earlier than the beginning date.
        """
        begin_date_obj = self._is_valid_date_format(beginning_date)
        end_date_obj = self._is_valid_date_format(end_date)

        if end_date_obj < begin_date_obj:
            raise ValueError(
                'Vacation end date cannot be earlier than the beginning date.')
        return begin_date_obj, end_date_obj

    def check_all_fields_but_image(self, vacation_id: str = None, country_id: str = None, vacation_description: str = None, beginning_date: str = None, end_date: str = None, price: int = None) -> None:
        """
        Checks if all required fields (except image) are provided and valid.

        Args:
            vacation_id (str): The ID of the vacation.
            country_id (str): The ID of the country.
            vacation_description (str): The description of the vacation.
            beginning_date (str): The beginning date of the vacation.
            end_date (str): The end date of the vacation.
            price (int): The price of the vacation.

        Raises:
            ValueError: If any required field is missing or invalid.
        """
        if vacation_id is None or country_id is None or vacation_description is None or beginning_date is None or end_date is None or price is None:
            raise ValueError("All fields are required.")
        if price <= 0:
            raise ValueError('Vacation cannot be priced 0 or lower.')
        if price > 10000:
            raise ValueError('Vacation cannot be priced higher than 10,000')

    def _create_vacation_dto_columns_and_values(self, vacation_id: str, country_id: str, vacation_description: str, beginning_date: str, end_date: str, price: int, picture_file_name: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """
        Creates a vacation DTO and returns the corresponding columns and values.

        Args:
            vacation_id (str): The ID of the vacation.
            country_id (str): The ID of the country.
            vacation_description (str): The description of the vacation.
            beginning_date (str): The beginning date of the vacation.
            end_date (str): The end date of the vacation.
            price (int): The price of the vacation.
            picture_file_name (str): The file name of the picture.

        Returns:
            tuple[tuple[str, ...], tuple[str, ...]]: A tuple of (columns, values).

        Raises:
            ValueError: If any required field is missing or invalid.
        """
        self.check_all_fields_but_image(
            vacation_id, country_id, vacation_description, beginning_date, end_date, price)
        if not picture_file_name:
            raise ValueError("All fields are required.")
        beginning_date_new, end_date_new = self._compare_dates(
            beginning_date, end_date)
        if beginning_date_new < datetime.datetime.today().date():
            raise ValueError(
                'Vacation beginning date cannot be earlier than today.')
        vacation_dto = vacations_dto.VacationDTO(
            vacation_id, country_id, vacation_description, beginning_date_new, end_date_new, price, picture_file_name)
        columns = ('vacation_id', 'country_id', 'vacation_description',
                   'beginning_date', 'end_date', 'price', 'picture_file_name')
        values = (vacation_dto.vacation_id, vacation_dto.country_id, vacation_dto.vacation_description, vacation_dto.vacation_beginning_date,
                  vacation_dto.vacation_end_date, vacation_dto.vacation_price, vacation_dto.vacation_image_filename)
        return columns, values

    def add_vacation(self, vacation_id: str = None, country_id: str = None, vacation_description: str = None, beginning_date: str = None, end_date: str = None, price: int = None, picture_file_name: str = None) -> None:
        """
        Adds a new vacation record.

        Args:
            vacation_id (str): The ID of the vacation.
            country_id (str): The ID of the country.
            vacation_description (str): The description of the vacation.
            beginning_date (str): The beginning date of the vacation.
            end_date (str): The end date of the vacation.
            price (int): The price of the vacation.
            picture_file_name (str): The file name of the picture.
        """
        columns, values = self._create_vacation_dto_columns_and_values(
            vacation_id, country_id, vacation_description, beginning_date, end_date, price, picture_file_name)
        self.vacation_dao.add(columns, values)

    def update_vacation(self, vacation_id: str = None, country_id: str = None, vacation_description: str = None, beginning_date: str = None, end_date: str = None, price: int = None, picture_file_name: str = None) -> None:
        """
        Updates an existing vacation record.

        Args:
            vacation_id (str): The ID of the vacation.
            country_id (str): The ID of the country.
            vacation_description (str): The description of the vacation.
            beginning_date (str): The beginning date of the vacation.
            end_date (str): The end date of the vacation.
            price (int): The price of the vacation.
            picture_file_name (str): The file name of the picture.
        """
        self.check_all_fields_but_image(
            vacation_id, country_id, vacation_description, beginning_date, end_date, price)
        beginning_date_new, end_date_new = self._compare_dates(
            beginning_date, end_date)
        if not self.vacation_dao.print_wanted_column_value_by_id('*', vacation_id):
            raise ValueError(f"Vacation with ID {vacation_id} does not exist.")

        if picture_file_name is not None:
            vacation_dto = vacations_dto.VacationDTO(
                vacation_id, country_id, vacation_description, beginning_date_new, end_date_new, price, picture_file_name)
            columns = ('vacation_id', 'country_id', 'vacation_description',
                       'beginning_date', 'end_date', 'price', 'picture_file_name')
            values = (vacation_dto.vacation_id, vacation_dto.country_id, vacation_dto.vacation_description, vacation_dto.vacation_beginning_date,
                      vacation_dto.vacation_end_date, vacation_dto.vacation_price, vacation_dto.vacation_image_filename)
            self.vacation_dao.update(columns, values, vacation_id)
        else:
            columns = ('vacation_id', 'country_id', 'vacation_description',
                       'beginning_date', 'end_date', 'price')
            values = (vacation_id, country_id, vacation_description,
                      beginning_date_new, end_date_new, price)
            self.vacation_dao.update(columns, values, vacation_id)
