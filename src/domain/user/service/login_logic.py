from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.common import auth, configs
from src.common.configs import KST
from src.db.entity.user_entity import UserEntity
from src.db.query.user import user_create, user_read

from ..model import user_response

config = configs.config.fastapi


async def identify_user(
    *,
    db: AsyncSession,
    form_data: OAuth2PasswordRequestForm,
) -> UserEntity:
    user = await user_read.read_user_by_name(
        db=db,
        name=form_data.username,
    )
    if user is None or not configs.pwd_context.verify(
        secret=form_data.password,
        hash=user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    await auth.verify_user_state(user=user)

    return user


async def create_login_history(
    *,
    db: AsyncSession,
    user_id: int,
) -> None:
    await user_create.create_login_his(
        db=db,
        user_id=user_id,
        created_datetime=datetime.now(KST),
    )


async def create_access_token(
    *,
    username: str,
) -> user_response.Token:
    data = {
        "sub": username,
        "exp": datetime.now(KST)
        + timedelta(minutes=int(config.auth.token_expire_minutes)),
    }
    access_token = jwt.encode(
        claims=data,
        key=config.auth.secret_key,
        algorithm=config.auth.algorithm,
    )
    token = user_response.Token(
        username=username,
        token_type="bearer",
        access_token=access_token,
    )
    return token
