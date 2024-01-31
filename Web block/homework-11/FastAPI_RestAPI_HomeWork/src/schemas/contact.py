from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field


class ContactSchema(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    surname: str = Field(min_length=1, max_length=150)
    email: EmailStr
    phone_number: str
    birth_date: date


class ContactResponse(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: EmailStr
    phone_number: str 
    birth_date: datetime

    class Config:
        from_attributes = True
