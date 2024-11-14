from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, Integer, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSON
from community_telegram_bot.database.models.base import Base
from enum import Enum

class GenderEnum(str, Enum):
    MAN = "Man"
    WOMAN = "Woman"
    BOTH = "Both"
    OTHER = "Other"

class Bio(Base):
    __tablename__ = 'bios'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[BigInteger] = mapped_column(ForeignKey('users.user_id'), unique=True, nullable=False, index=True) 
    profile_name: Mapped[str] = mapped_column(String(50), nullable=False)
    profile_age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(SQLEnum(GenderEnum, name="gender_enum"), nullable=False)
    profile_bio: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[str] = mapped_column(String(15))
    longitude: Mapped[str] = mapped_column(String(15))
    profile_city: Mapped[str] = mapped_column(String(50), nullable=False)
    profile_region: Mapped[str] = mapped_column(String(50))
    profile_country: Mapped[str] = mapped_column(String(50))
    user = relationship("User", back_populates="bio", uselist=False)
    photos: Mapped[List["BioPhoto"]] = relationship(back_populates="bio", cascade="all, delete-orphan")
    likes_sent: Mapped[List["Like"]] = relationship(back_populates="like_sender_bio", cascade="all, delete-orphan", foreign_keys='Like.like_sender_bio_id')
    likes_received: Mapped[List["Like"]] = relationship(back_populates="liked_bio", cascade="all, delete-orphan", foreign_keys='Like.like_receiver_bio_id')

class BioPhoto(Base):
    __tablename__ = 'bios_photos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bio_id: Mapped[int] = mapped_column(Integer, ForeignKey('bios.id'), nullable=False)
    photo_id: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped["Bio"] = relationship(back_populates="photos", foreign_keys=[bio_id])

class Like(Base):
    __tablename__ = 'likes'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    like_sender_bio_id: Mapped[int] = mapped_column(ForeignKey('bios.id'), nullable=False)
    like_receiver_bio_id: Mapped[int] = mapped_column(ForeignKey('bios.id'), nullable=False)
    is_match: Mapped[Boolean] = mapped_column(Boolean, default=False)
    like_sender_bio: Mapped["Bio"] = relationship(back_populates="likes_sent", foreign_keys=[like_sender_bio_id])
    like_receiver_bio: Mapped["Bio"] = relationship(back_populates="likes_received", foreign_keys=[like_receiver_bio_id])

class FriendshipSearchFilter(Base):
    __tablename__ = 'friendships_search_filter'
    user_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey('users.user_id'), primary_key=True, index=True)
    city: Mapped[str] = mapped_column(String(50), nullable=True)
    region: Mapped[str] = mapped_column(String(50), nullable=True)
    country: Mapped[str] = mapped_column(String(50), nullable=True)
    search_id_list: Mapped[list] = mapped_column(JSON, nullable=True)  # List of IDs the user has already seen
    city_search: Mapped[bool] = mapped_column(Boolean, default=True)
    gender: Mapped[GenderEnum] = mapped_column(SQLEnum(GenderEnum, name="gender_enum"), nullable=False)