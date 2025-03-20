

from dataclasses import dataclass


@dataclass
class UserDTO:
    user_id: str
    first_name: str
    last_name: str
    user_email: str
    password: str
    role_id: str
