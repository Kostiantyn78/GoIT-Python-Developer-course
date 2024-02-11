import unittest
from unittest.mock import MagicMock, AsyncMock, Mock, ANY
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema
from src.repository.contact import (create_contact, get_contact, update_contact, delete_contact, get_contacts, 
                                    search_contacts, get_contacts_birthdays_for7days)


class TestAsyncContact(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = User(id=1, username='test_user', password="55555", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contact(id=1, name='test_record_1', surname='test_record_1', email='test_record_1@gmail.com', 
                            phone_number="+380501111111", birth_date=date(1981, 1, 11), user=self.user),
                    Contact(id=2, name='test_record_2', surname='test_record_2', email='test_record_2@gmail.com',
                            phone_number="+380952222222", birth_date=date(1982, 2, 22), user=self.user)]
        mocked_contacts = Mock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactSchema(name='test_record_1', surname='test_record_1', email='test_record_1@gmail.com',
                             phone_number="+380501111111", birth_date=date(1981, 1, 11))
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.email, body.email)

    async def test_update_contact(self):
        body = ContactSchema(name='test_record_1', surname='test_record_1', email='test_record_1@gmail.com',
                             phone_number="+380501111111", birth_date=date(1981, 1, 11))
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, name='test_record_U1', surname='test_record_U1',
                                                                 email='test_record_1@gmail.com',
                                                                 phone_number="+380501111111",
                                                                 birth_date=date(1981, 1, 11))
        self.session.execute.return_value = mocked_contact
        result = await update_contact(1, body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.email, body.email)

    async def test_delete_contact(self):
        mocked_todo = MagicMock()
        mocked_todo.scalar_one_or_none.return_value = Contact(id=1, name='test_record_U1', surname='test_record_U1',
                                                              email='test_record_1@gmail.com',
                                                              phone_number="+380501111111",
                                                              birth_date=date(1981, 1, 11),
                                                              user=self.user)
        self.session.execute.return_value = mocked_todo
        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, Contact)

    async def test_get_contact(self):
        contact = Contact(id=1, name='test_record_1', surname='test_record_1', email='test_record_1@gmail.com',
                          phone_number="+380501111111", birth_date=date(1981, 1, 11), user=self.user)
        mocked_contacts = Mock()
        mocked_contacts.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contacts
        result = await get_contact(contact_id=1, db=self.session, user=self.user)
        self.assertEqual(result, contact)

    async def test_get_contacts_birthday(self):
        limit = 10
        offset = 0
        contacts = [Contact(id=1, name='test_record_1', surname='test_record_1', email='test_record_1@gmail.com',
                            phone_number="+380501111111", birth_date=date(1981, 1, 11), user=self.user),
                    Contact(id=2, name='test_record_2', surname='test_record_2', email='test_record_2@gmail.com',
                            phone_number="+380952222222", birth_date=date(1982, 2, 22), user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts_birthdays_for7days(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_get_contacts_select(self):
        contacts = [Contact(id=1, name='test_record_1', surname='test_record_1', email='test_record_1@gmail.com',
                            phone_number="+380501111111", birth_date=date(1981, 1, 11), user=self.user),
                    Contact(id=2, name='test_record_2', surname='test_record_2', email='test_record_2@gmail.com',
                            phone_number="+380952222222", birth_date=date(1982, 2, 22), user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await search_contacts(name='test_record_1', surname='test_record_1', email='test_record_1@gmail.com',
                                       limit=10, offset=0, db=self.session, user=self.user)
        expected_query = (
        select(Contact)
                    .filter_by(user=self.user)
                    .filter(Contact.name.ilike('%test_record_1%'))
                    .filter(Contact.surname.ilike('%test_record_1%'))
                    .filter(Contact.email.ilike('%test_record_1@gmail.com%'))
                    .offset(0)
                    .limit(10)
                    )
        self.session.execute.assert_called_once_with(ANY)
        actual_query = self.session.execute.call_args[0][0]

        self.assertEqual(str(actual_query), str(expected_query))
        self.assertEqual(result, contacts)
        