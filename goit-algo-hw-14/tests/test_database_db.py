import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncEngine,AsyncSession,async_sessionmaker,create_async_engine
from src.database.db import DatabaseSessionManager

class TestDatabaseSessionManager (unittest.TestCase):
	def setUp (self):
		self.url = "sqlite+aiosqlite:///:memory:"
		self.database_session_manager = DatabaseSessionManager (self.url)

	@patch ('src.database.db.create_async_engine')
	@patch ('src.database.db.async_sessionmaker')
	async def test_session (self,
			mock_async_sessionmaker,
			mock_create_async_engine):
		mock_engine = AsyncMock (AsyncEngine)
		mock_create_async_engine.return_value = mock_engine
		mock_session = AsyncMock (AsyncSession)
		mock_async_sessionmaker.return_value = MagicMock (return_value=mock_session)

		async with self.database_session_manager.session () as session:
			self.assertEqual (session,
				mock_session)

		mock_create_async_engine.assert_called_once_with (self.url)
		mock_async_sessionmaker.assert_called_once_with (autoflush=False,
			autocommit=False,
			bind=mock_engine)
		mock_session.close.assert_called_once ()

	def tearDown (self):
		pass

if __name__ == '__main__':
	unittest.main ()
