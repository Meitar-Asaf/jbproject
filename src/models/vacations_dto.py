from dataclasses import dataclass
import datetime


@dataclass
class VacationDTO:
    vacation_id: str
    country_id: str
    vacation_description: str
    vacation_beginning_date: datetime.date
    vacation_end_date: datetime.date
    vacation_price: int
    vacation_image_filename: str
