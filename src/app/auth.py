from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from jose import jwt, JWTError

from settings.config import auth_config
from settings.database import get_db
from src.crud import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/user/login')


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, auth_config.secret_key, algorithms=[auth_config.algorithm])
        username: str = str(payload.get('sub'))
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = await get_user(db, username)
        if user is None:
            raise credentials_exception
        return user