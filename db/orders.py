from enum import Enum

from sqlalchemy import Integer, BigInteger, Enum as AsEnum, ForeignKey, SMALLINT, and_, select
from sqlalchemy.orm import relationship, mapped_column, Mapped

from db.base import db, CreatedModel


class Order(CreatedModel):
    class OrderStatusEnum(Enum):
        PENDING = "Pending"
        APPROVED = "Approved"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(AsEnum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped['User'] = relationship("User", back_populates="orders")
    order_items: Mapped[list['OrderItem']] = relationship("OrderItem", back_populates="order")

    @classmethod
    async def get(cls, user_id):
        query = select(cls).where(and_(cls.user_id == user_id, cls.status == cls.OrderStatusEnum.PENDING))
        return (await db.execute(query)).scalar()


class OrderItem(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    count: Mapped[int] = mapped_column(SMALLINT, default=1)
    book_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("books.id", ondelete="CASCADE"))
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    book: Mapped['Book'] = relationship("Book", back_populates="order_items")
    order: Mapped['Order'] = relationship("Order", back_populates="order_items")

    @classmethod
    async def filter(cls, order_id):
        query = select(cls).where(cls.order_id == order_id)
        objects = await db.execute(query)
        result = []
        for i in objects.all():
            result.append(i[0])
        return result
