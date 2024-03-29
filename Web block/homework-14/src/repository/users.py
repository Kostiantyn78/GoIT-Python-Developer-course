from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.database.db import get_db
from src.entity.models import User
from src.schemas.user import UserSchema
from libgravatar import Gravatar


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    The get_user_by_email function takes an email address and returns the user object associated with that email.
    If no such user exists, it returns None.

    :param email: str: Pass the email of the user to be retrieved
    :param db: AsyncSession: Pass the database session to the function
    :return: A single user
    """
    statement = select(User).filter_by(email=email)
    user = await db.execute(statement)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    The create_user function creates a new user in the database.

    :param body: UserSchema: Validate the incoming request body
    :param db: AsyncSession: Pass in the database session
    :return: The newly created user object
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Specify the user object that will be updated
    :param token: str | None: Update the user's refresh token
    :param db: AsyncSession: Pass the database session to the function
    :return: The user object
    """
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    The confirmed_email function takes an email address and a database connection,
    and marks the user with that email as confirmed.  It does not return anything.

    :param email: str: Specify the email of the user to be confirmed
    :param db: AsyncSession: Pass the database session to the function
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    """
    The update_avatar_url function updates the avatar URL for a user.

    :param email: str: Get the user from the database
    :param url: str | None: Specify that the url parameter is either a string or none
    :param db: AsyncSession: Pass the database session into the function
    :return: A user object, which is the updated user
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user


async def new_password(email: str, new_password: str, db: AsyncSession= Depends(get_db)):
    """
    The new_password function takes an email and a new password,
        then updates the user's password in the database.

    :param email: str: Get the email of the user who wants to change their password
    :param new_password:str: Pass in the new password
    :param db: AsyncSession: Pass the database session into the function
    :return: The updated user object
    """
    user = await get_user_by_email(email, db)
    user.password = new_password
    await db.commit()
    await db.refresh(user)
    return user
