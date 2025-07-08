from database import Base, engine, Session
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy_utils import ChoiceType # type: ignore
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    orders = relationship('Order', back_populates='user')

    def __repr__(self):
        return f"<User {self.username} - {self.email}>"
    
class Order(Base):

    ORDER_STATUSES = (
        ('PENDING', 'pending'),
        ('IN-TRANSIT', 'in-Transit'),
        ('DELIVERED', 'delivered'),
    )

    PIZZA_SIZES = (
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('EXTRA_LARGE', 'extra_large'),
    )

    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices = ORDER_STATUSES), default='PENDING')
    pizza_size = Column(ChoiceType(choices = PIZZA_SIZES), default='SMALL')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='orders')

    def __repr__(self):
        return f"<Order {self.id} - {self.order_status}>"