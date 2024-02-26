from sqlalchemy import String, DateTime
from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[String] = mapped_column(String(20))
    surname: Mapped[String] = mapped_column(String(20))
    email: Mapped[String] = mapped_column(String(40))
    phone: Mapped[String] = mapped_column(String(30))
    born_date: Mapped[datetime] = mapped_column(DateTime)
