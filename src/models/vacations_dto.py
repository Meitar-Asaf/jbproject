from dataclasses import dataclass


@dataclass
class VacationDTO:
    vacation_id: str
    country_id: str
    vacation_description: str
    vacation_beginning_date: str
    vacation_end_date: str
    vacation_price: int
    vacation_image_filename: str
