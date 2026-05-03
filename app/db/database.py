from sqlalchemy.types import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from app.config import config

DATABASE_URL = config["DATABASE_URL"]

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

class Product(Base):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[str] = mapped_column(Float(3), nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False, default='None')