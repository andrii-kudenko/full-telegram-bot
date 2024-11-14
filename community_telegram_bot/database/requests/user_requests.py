from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import BigInteger
from ..models import User

async def get_user_by_user_id(db: AsyncSession, user_id: BigInteger) -> User | None:
    """Fetch a user by their user_id."""
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_id: BigInteger, name: str):
    """Create a new user."""
    new_user = User(user_id=user_id, name=name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user_name(db: AsyncSession, user_id: BigInteger, new_name: str):
    """Update the user's name."""
    user = await get_user_by_user_id(db, user_id)
    if user:
        user.name = new_name
        await db.commit()
    return user




