import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

import os
import sys
sys.path.append(os.path.abspath('../HW_M11'))

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    remove_contact,
    get_contacts_bdays)


class TestContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact(), Contact()]

        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(name="<NAME>", surname="<SURNAME>", email="0953226763r@gmail.com", phone="+380683226263",
                            born_date="2022-08-08")
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.born_date, body.born_date)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_contact_found(self):
        body = ContactModel(name="<NAME1>", surname="<SURNAME1>", email="0953226763r@gmail.com", phone="+380683226263",
                            born_date="2022-08-08")
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactModel(name="<NAME1>", surname="<SURNAME1>", email="0953226763r@gmail.com", phone="+380683226263",
                            born_date="2022-08-08")
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contacts_bdays(self):
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        str_date = tomorrow.strftime("%Y-%m-%d")
        contact = Contact(born_date=str_date)
        self.session.query().filter().all.return_value = contact
        result = await get_contacts_bdays(user=self.user, db=self.session)
        self.assertEqual(result, contact)


if __name__ == '__main__':
    unittest.main()
