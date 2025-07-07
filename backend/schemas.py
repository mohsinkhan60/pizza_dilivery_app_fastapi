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
    password: str
    is_staff: bool
    is_active: bool

    class Config:
        from_attributes = True

class Settings(BaseModel):
    authjwt_secret_key: str = "a4d4b888f376b77a9c425c42fc39f2a286cc48301a3246cf3669cc4024609407"

class LoginModel(BaseModel):
    username: str
    password: str

    # class Config:
    #     from_attributes = True
    #     json_schema_extra = {
    #         'example': {
    #             "username": "johndoe",
    #             "password": "password"
    #         }
    #     }