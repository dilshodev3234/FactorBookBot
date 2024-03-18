from enum import Enum

from sqlalchemy import Integer, BigInteger, VARCHAR, ForeignKey, Text, Enum as AsEnum, FLOAT, select, \
    SmallInteger
from sqlalchemy.orm import relationship, mapped_column, Mapped

from db.base import db, CreatedModel
from web.utils import CustomImageField


class Category(CreatedModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped['User'] = relationship("User", back_populates="categories")
    books: Mapped[list['Book']] = relationship("Book", back_populates="category")


class Book(CreatedModel):
    class VolEnum(Enum):
        HARD = "Hard"
        SOFT = "Soft"

    class MoneyEnum(Enum):
        DOLLAR = "$"
        CENT = "¢"
        SUM = "S"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(255), index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    photo: Mapped[str] = mapped_column(CustomImageField)
    price: Mapped[float] = mapped_column(FLOAT, nullable=False)
    money_type: Mapped[str] = mapped_column(AsEnum(MoneyEnum, values_callable=lambda i: [field.value for field in i]),
                                            default=MoneyEnum.SUM)
    amount: Mapped[int] = mapped_column(SmallInteger, server_default='1')
    vol: Mapped[str] = mapped_column(AsEnum(VolEnum, values_callable=lambda i: [field.value for field in i]),
                                     default=VolEnum.SOFT)
    page: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categorys.id", ondelete="CASCADE"))
    category: Mapped['Category'] = relationship("Category", back_populates="books")
    order_items: Mapped[list['OrderItem']] = relationship("OrderItem", back_populates="book")

    @classmethod
    async def filter(cls, category_id):
        query = select(cls).where(cls.category_id == category_id)
        return (await db.execute(query)).scalars()
