from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from .settings import config


engine = create_async_engine(
    url=config.db.url,
    echo=False,
    pool_pre_ping=True,
    pool_size=50,
    max_overflow=0
)

session_fabric = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_session():
    async with session_fabric() as session:
        yield session