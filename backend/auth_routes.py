from fastapi import APIRouter
from database import Session
from schemas import SignUpModel, UserResponseModel
from models import User
from fastapi import HTTPException, status
from werkzeug.security import generate_password_hash, check_password_hash

auth_router = APIRouter(
      prefix="/auth",
      tags=["auth"]
)

session = Session()

@auth_router.get("/")
async def auth():
    return {"message": "auth endpoint"}

@auth_router.post("/signup", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )
    session.add(new_user)
    session.commit()
    return new_user