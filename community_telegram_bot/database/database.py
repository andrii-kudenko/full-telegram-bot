from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# *Load database url
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Use async session
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency to get async DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
