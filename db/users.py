from datetime import datetime
from enum import Enum
from sqlalchemy import Integer, Enum as AsEnum, BigInteger, VARCHAR, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

from db.base import AbstractClass, CreatedModel, Base


class User(CreatedModel):
    class LangEnum(Enum):
        EN = "en"
        UZ = "uz"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(255))
    full_name: Mapped[str] = mapped_column(VARCHAR(255))
    lang: Mapped[str] = mapped_column(AsEnum(LangEnum, values_callable=lambda i: [field.value for field in i]),
                                      default=LangEnum.EN, nullable=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    orders: Mapped[list['Order']] = relationship("Order", back_populates="user")
    categories: Mapped[list['Category']] = relationship("Category", back_populates="owner")

    def __str__(self):
        return f"{self.full_name}"


class DeleteUser(Base, AbstractClass):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    deleted_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)


class Network(CreatedModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    link: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
