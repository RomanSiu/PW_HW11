from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import datetime

PhoneNumber.phone_format = "E164"


class UserModel(BaseModel):
    name: str = Field(max_length=30)
    surname: str = Field(max_length=30)
    email: EmailStr = Field(default=None)
    phone: PhoneNumber = Field(max_length=13)
    born_date: datetime = Field()
