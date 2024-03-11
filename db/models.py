from datetime import datetime
from sqlalchemy import Integer, BigInteger, VARCHAR, ForeignKey, Text, DECIMAL, Enum, SMALLINT, DateTime, FLOAT
from sqlalchemy.orm import relationship, mapped_column, Mapped
from config.enums.main import LangEnum, MoneyEnum, VolEnum, OrderStatusEnum
from db.utils import CreatedModel, Base
from db.utils import AbstractClass


class User(CreatedModel):
    __tablename__ = "users"  # noqa
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(255))
    full_name: Mapped[str] = mapped_column(VARCHAR(255))
    lang: Mapped[str] = mapped_column(Enum(LangEnum), default=LangEnum.EN.name)
    phone_number: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    orders: Mapped[list['Order']] = relationship("Order", back_populates="user")


class Category(CreatedModel):
    __tablename__ = "categories"  # noqa
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    books: Mapped[list['Book']] = relationship("Book", back_populates="category")


class Book(CreatedModel):
    __tablename__ = "books"  # noqa
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    photo: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    price: Mapped[float] = mapped_column(FLOAT, nullable=False)
    money_type: Mapped[str] = mapped_column(Enum(MoneyEnum), default=MoneyEnum.SUM.name)
    amount: Mapped[int] = mapped_column(SMALLINT, default=1)
    vol: Mapped[str] = mapped_column(Enum(VolEnum), default=VolEnum.SOFT)
    page: Mapped[int] = mapped_column(default=VolEnum.SOFT)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categories.id", ondelete="CASCADE"))
    category: Mapped['Category'] = relationship("Category", back_populates="books")
    orders: Mapped[list['Order']] = relationship("Order", back_populates="book")


#
#
class Order(CreatedModel):
    __tablename__ = "orders"  # noqa
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    count: Mapped[int] = mapped_column(SMALLINT, default=1)
    status: Mapped[str] = mapped_column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    book_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("books.id", ondelete="CASCADE"))
    user: Mapped['User'] = relationship("User", back_populates="orders")
    book: Mapped['Book'] = relationship("Book", back_populates="orders")


class DeleteUser(Base, AbstractClass):
    __tablename__ = "delete_users"  # noqa
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    deleted_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)


class Network(CreatedModel):
    __tablename__ = "networks"  # noqa
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    link: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
