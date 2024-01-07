import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema
from src.repository.contacts import create_contact, update_contact, delete_contact, get_contacts


class TestAsyncContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(id=1, username='test_user', password="qwerty", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contact(id=1, first_name='test_first_name_1', last_name='test_last_name_1', email='test_email_1',
                            phone='test_phone_1', birthday='test_birth_1', user=self.user),
                    Contact(id=2, first_name='test_first_name_2', last_name='test_last_name_2', email='test_email_2',
                            phone='test_phone_2', birthday='test_birth_2', user=self.user)]
        mocked_contact = MagicMock()
        mocked_contact.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contact
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactSchema(first_name='test_first_name_1', last_name='test_last_name_1', email='test_email_1',
                             phone='test_phone_1', birthday='test_birth_1')
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)

    async def test_update_contact(self):
        body = ContactUpdateSchema(first_name='test_first_name_1', last_name='test_last_name_1', email='test_email_1',
                                   phone='test_phone_1', birthday='test_birth_1', completed=True)
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, first_name='test_first_name_1',
                                                                 last_name='test_last_name_1', email='test_email_1',
                                                                 phone='test_phone_1', birthday='test_birth_1',
                                                                 user=self.user)
        self.session.execute.return_value = mocked_contact
        result = await update_contact(1, body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)

    async def test_delete_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, first_name='test_first_name_1',
                                                                 last_name='test_last_name_1', email='test_email_1',
                                                                 phone='test_phone_1', birthday='test_birth_1',
                                                                 user=self.user)
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()

        self.assertIsInstance(result, Contact)
