from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from src.schemas.user import UserResponse


class ContactSchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=3, max_length=100)
    phone: str = Field(min_length=10, max_length=13)
    birthday: str = Field(min_length=3, max_length=13)
    completed: Optional[bool] = False


class ContactUpdateSchema(ContactSchema):
    completed: bool


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: str
    completed: bool
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None
    model_config = ConfigDict(from_attributes=True)
