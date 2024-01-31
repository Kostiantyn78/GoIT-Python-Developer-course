from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.entity.models import Contact
from src.schemas.contact import ContactSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    query = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(query)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    query = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(query)
    return contact.scalar_one_or_none()


async def get_contacts_birthdays_for7days(limit: int, offset: int, db: AsyncSession):
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
    query = (
        select(Contact)
        .filter(Contact.birth_date.between(today, end_date))
    )
    query = query.offset(offset).limit(limit)
    contacts = await db.execute(query)
    return contacts.scalars().all()


async def search_contacts(name: str, surname: str, email: str, limit: int, offset: int, db: AsyncSession):
    query = select(Contact)
    if name:
        query = query.filter(Contact.name.ilike(f'%{name}%'))
    if surname:
        query = query.filter(Contact.surname.ilike(f'%{surname}%'))
    if email:
        query = query.filter(Contact.email.ilike(f'%{email}%'))
    query = query.offset(offset).limit(limit)
    contacts = await db.execute(query)
    return contacts.scalars().all()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession):
    query = select(Contact).filter_by(id=contact_id)
    result = await db.execute(query)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birth_date = body.birth_date
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    query = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(query)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
