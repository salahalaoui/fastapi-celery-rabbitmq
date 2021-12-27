from fastapi import APIRouter

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status

from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

from ..database import db_context

from ..config import settings
from jose import JWTError, jwt
from ..schema import TokenData, Token, User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..models import ModelUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

router = APIRouter(
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str):
    user = ModelUser.get_user_by_username(username)

    if not user or not user.check_password(password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = ModelUser.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user



@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register/")
def register(user: User):

    existing_user = ModelUser.get_user_by_username(user.name)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    with db_context() as session:
        db_user = ModelUser(name=user.name)
        db_user.set_password(user.password)

        session.add(db_user)
        session.commit()
    return
