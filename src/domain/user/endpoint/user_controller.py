from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src import dependency
from src.core import auth
from src.core.model.enums import ResponseEnum

from ..business import user_process
from ..model import user_request, user_response

router = APIRouter(prefix="/user")


@router.post(path="", status_code=status.HTTP_201_CREATED)
async def create_user(
    repo: dependency.UserRepo,
    body: Annotated[user_request.UserCreateRequest, Body()],
) -> ResponseEnum:
    """
    - one email can be used by only one user
    - username cannot be used if one is occupied
    - PW1 and PW2 mush be same
    """
    await user_process.create_user(repo=repo, data=body)
    return ResponseEnum.CREATE


@router.post(path="/login")
async def login_user(
    repo: dependency.UserRepo,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> user_response.Token:
    token = await user_process.login_user(repo=repo, form_data=form_data)
    return token


@router.put(path="")
async def update_user(
    current_user: auth.CurrentUser,
    repo: dependency.UserRepo,
    cache: dependency.CacheRepo,
    body: Annotated[user_request.UserBase, Body()],
) -> ResponseEnum:
    await user_process.update_user(
        user=current_user,
        repo=repo,
        cache=cache,
        data=body,
    )
    return ResponseEnum.UPDATE


@router.put(path="/password")
async def update_password(
    current_user: auth.CurrentUser,
    repo: dependency.UserRepo,
    cache: dependency.CacheRepo,
    body: Annotated[user_request.Password, Body()],
) -> ResponseEnum:
    await user_process.update_password(
        user=current_user,
        repo=repo,
        cache=cache,
        data=body,
    )
    return ResponseEnum.UPDATE


@router.delete(path="")
async def resign_user(
    current_user: auth.CurrentUser,
    repo: dependency.UserRepo,
    cache: dependency.CacheRepo,
) -> ResponseEnum:
    await user_process.resign_user(user=current_user, repo=repo, cache=cache)
    return ResponseEnum.DELETE
