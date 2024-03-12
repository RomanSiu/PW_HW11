import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

import os
import sys
sys.path.append(os.path.abspath('../HW_M11'))

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_avatar)


class TestUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_user_by_email_found(self):
        user = User(email="0953226763r@gmail.com")
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email="0953226763r@gmail.com", db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email="0953226763r@gmail.com", db=self.session)
        self.assertIsNone(None)

    async def test_create_user(self):
        body = UserModel(username="<NAME>", email="0953226763r@gmail.com", password="<PASSWORD>")
        result = await create_user(body=body, db=self.session)
        self.assertEqual(body.username, result.username)
        self.assertEqual(body.email, result.email)
        self.assertEqual(body.password, result.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_avatar(self):
        user = User(avatar="avatar.com")
        self.session.query().filter().first.return_value = user
        result = await update_avatar(email="0953226763r@gmail.com", url="avatar.com", db=self.session)
        self.assertEqual(result, user)


if __name__ == "__main__":
    unittest.main()
