from fastapi import APIRouter, Depends
from database import Session
from schemas import SignUpModel, UserResponseModel, LoginModel
from models import User
from fastapi import HTTPException, status
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT  # type: ignore
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(
      prefix="/auth",
      tags=["auth"]
)

session = Session()

@auth_router.get("/")
async def auth(Authorize: AuthJWT = Depends()):
    """
    ## A simple Hello World route to test JWT authentication.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Hellow Mohsin Khan, this is your auth route!"}


@auth_router.post("/signup", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    """
    ## Create a User.
    This requires the folliwing
    ```
    - username: str
    - email: str
    - password: str
    - is_staff: Optional[bool] = False
    - is_active: Optional[bool] = True
    ```
    """
    # Check for existing email
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Check for existing username
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )

    # Create new user
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)  # ✅ Important to get the ID after commit

    # Return serialized response matching UserResponseModel
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "password": new_user.password,  # Note: Password should not be returned in production
        "is_staff": new_user.is_staff,
        "is_active": new_user.is_active
    }


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    """
    ## Login a User.
    This requires the folliwing
    ```
    - username: str
    - password: str
    ```
    and returns an access token and a refresh token.
    """
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        return jsonable_encoder({
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

@auth_router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(Authorize: AuthJWT = Depends()):
    """
    ## Create a Fresh Token.
    This creates a fresh access token using the refresh token.
    """
    try:
        Authorize.jwt_refresh_token_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({
        "access_token": access_token
    })
