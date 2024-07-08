import contextlib
from sqlalchemy.ext.asyncio import AsyncEngine,async_sessionmaker,create_async_engine
from src.conf.config import config

class DatabaseSessionManager:
    def __init__(self, url: str):
        """
        Initialize a DatabaseSessionManager instance.

        Args:
            url (str): The database connection URL.

        Attributes:
            _engine (AsyncEngine | None): The SQLAlchemy async engine instance.
            _session_maker (async_sessionmaker): The SQLAlchemy async session maker instance.
        """
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(autoflush=False,
                                                                     autocommit=False,
                                                                     bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self):
        """
        Asynchronous context manager for handling database sessions.

        This method creates an asynchronous database session using the SQLAlchemy async session maker.
        It ensures that the session is properly initialized, committed, or rolled back, and closed after use.

        Raises:
            Exception: If the session maker is not initialized.

        Yields:
            AsyncSession: The asynchronous database session.

        Example:
            async with sessionmanager.session() as session:
                # Perform database operations using the session
                result = await session.query(User).filter_by(name='John').first()
                print(result)
        """
        if self._session_maker is None:
            raise Exception("Session is not initialized")

        session = self._session_maker()

        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()

sessionmanager = DatabaseSessionManager(config.SQLALCHEMY_DATABASE_URL)

async def get_db():
    """
    Dependency function for getting a database session.

    This function is used as a dependency in FastAPI endpoints to provide a database session
    for the request lifecycle. It uses the `sessionmanager` instance to create an asynchronous
    database session using the SQLAlchemy async session maker. The session is automatically
    committed or rolled back, and closed after use.

    Yields:
        AsyncSession: The asynchronous database session.

    Example:
        async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
            user = await db.query(User).filter(User.id == user_id).first()
            return user

    Note:
        The `get_db` function should be used as a dependency in FastAPI endpoints to ensure
        that a database session is available for each request.

    """
    async with sessionmanager.session() as session:
        yield session
