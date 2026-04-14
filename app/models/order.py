from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Cart(Base):
    __tablename__="cart"
    __table_args__=(
        UniqueConstraint('user_id','product_id', name='unique_user-product'),
        CheckConstraint('quantity>0', name='check_cart_quantity_positive'),
    )
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, default=1, nullable=False)

    product = relationship("Product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(String(20), default="pending", nullable=False, index=True)
    razorpay_order_id = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User")
    items = relationship("OrderItem", backref="order", cascade="all, delete")


class OrderItem(Base):
    __tablename__ = "order_items"

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_orderitem_quantity_positive'),
    )

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    product = relationship("Product")