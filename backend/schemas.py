from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }


class UserResponseModel(BaseModel):
    id: int
    username: str
    email: str
    is_staff: bool
    is_active: bool

    class Config:
        from_attributes = True

