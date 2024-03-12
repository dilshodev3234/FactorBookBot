from datetime import datetime

from sqlalchemy import Integer, BigInteger, VARCHAR, ForeignKey, Text, Enum, SMALLINT, DateTime, FLOAT
from sqlalchemy.orm import relationship, mapped_column, Mapped

from db.enums.main import LangEnum, MoneyEnum, VolEnum, OrderStatusEnum
from db.utils import AbstractClass, CreatedModel, Base


class User(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(255))
    full_name: Mapped[str] = mapped_column(VARCHAR(255))
    lang: Mapped[str] = mapped_column(Enum(LangEnum), default=LangEnum.EN, nullable=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    orders: Mapped[list['Order']] = relationship("Order", back_populates="user")
    categories: Mapped[list['Category']] = relationship("Category", back_populates="owner")


class Category(CreatedModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped['User'] = relationship("User", back_populates="categories")
    books: Mapped[list['Book']] = relationship("Book", back_populates="category")


class Book(CreatedModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    photo: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    price: Mapped[float] = mapped_column(FLOAT, nullable=False)
    money_type: Mapped[str] = mapped_column(Enum(MoneyEnum), default=MoneyEnum.SUM.name)
    amount: Mapped[int] = mapped_column(SMALLINT, default=1)
    vol: Mapped[str] = mapped_column(Enum(VolEnum), default=VolEnum.SOFT)
    page: Mapped[int] = mapped_column(default=VolEnum.SOFT)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categorys.id", ondelete="CASCADE"))
    category: Mapped['Category'] = relationship("Category", back_populates="books")
    orders: Mapped[list['Order']] = relationship("Order", back_populates="book")


class Order(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    count: Mapped[int] = mapped_column(SMALLINT, default=1)
    status: Mapped[str] = mapped_column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    book_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("books.id", ondelete="CASCADE"))
    user: Mapped['User'] = relationship("User", back_populates="orders")
    book: Mapped['Book'] = relationship("Book", back_populates="orders")


class DeleteUser(Base, AbstractClass):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    deleted_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)


class Network(CreatedModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    link: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
