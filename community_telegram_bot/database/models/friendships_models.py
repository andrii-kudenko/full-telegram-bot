from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, Integer, Boolean, ForeignKey
from community_telegram_bot.database.models.base import Base

class Bio(Base):
    __tablename__ = 'bios'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[BigInteger] = mapped_column(ForeignKey('users.user_id'), unique=True, nullable=False, index=True) 
    profile_name: Mapped[str] = mapped_column(String(50), nullable=False)
    profile_bio: Mapped[str] = mapped_column(String(255), nullable=False)
    profile_age: Mapped[int] = mapped_column(Integer, nullable=False)
    latitude: Mapped[str] = mapped_column(String(15))
    longitude: Mapped[str] = mapped_column(String(15))
    profile_city: Mapped[str] = mapped_column(String(50), nullable=False)
    search_id: Mapped[int] = mapped_column(Integer)
    beyond_city_search_id: Mapped[int] = mapped_column(Integer)
    city_search: Mapped[Boolean] = mapped_column(Boolean, default=True)
    user = relationship("User", back_populates="bio", uselist=False)
    # photos: Mapped[List["BioPhoto"]] = relationship(back_populates="bio", cascade="all, delete-orphan")
    # likes: Mapped["Like"] = relationship(back_populates="bio", cascade="all, delete-orphan", foreign_keys='Like.bio_id')
    # liked_by: Mapped["Like"] = relationship(back_populates="liked_bio", cascade="all, delete-orphan", foreign_keys='Like.liked_bio_id')