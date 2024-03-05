from sqlalchemy import String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from datetime import datetime


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[String] = mapped_column(String(20))
    surname: Mapped[String] = mapped_column(String(20))
    email: Mapped[String] = mapped_column(String(40))
    phone: Mapped[String] = mapped_column(String(30))
    born_date: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("users.id", ondelete="CASCADE"),
                                         default=None)
    user = relationship("User", backref="contacts")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[String] = mapped_column(String(50))
    email: Mapped[String] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[String] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    refresh_token: Mapped[String] = mapped_column(String(255), nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    avatar: Mapped[String] = mapped_column(String(255), nullable=True)
