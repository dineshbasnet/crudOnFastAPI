from sqlmodel import create_engine, text,SQLModel
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine




async_engine:AsyncEngine = create_async_engine(

    url=Config.DATABASE_URL,
    echo=True
)


async def init_db():
    async with async_engine.begin() as conn:
        from src.books.models import Book
        
        await conn.run_sync(SQLModel.metadata.create_all)
        
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session