from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.repository import contact as repository_contacts
from src.schemas.contact import ContactResponse, ContactSchema
from src.services.auth import auth_service

from src.entity.models import User, Role
from src.services.roles import RoleAccess
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/contacts', tags=['contacts'])

access_to_route_all = RoleAccess([Role.admin, Role.moderator])


@router.get("/", response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(limit, offset, db, current_user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CONTACT NOT FOUND")
    return contact


@router.get("/birthdays_for7days", response_model=list[ContactResponse],
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts_birthdays_for7days(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                                          db: AsyncSession = Depends(get_db),
                                          current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts_birthdays_for7days(limit, offset, db, current_user)
    return contacts


@router.get("/search/", response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts_select(
        name: str = Query(None, description="Search by name"),
        surname: str = Query(None, description="Search by surname"),
        email: str = Query(None, description="Search by email"),
        limit: int = Query(10, ge=10, le=500),
        offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):
    contacts_get = await repository_contacts.search_contacts(name, surname, email, limit, offset, db, current_user)
    return contacts_get


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.create_contact(body, db, current_user)
    return contact


@router.put("/{contact_id}", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CONTACT NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.delete_contact(contact_id, db, current_user)
    return contact
