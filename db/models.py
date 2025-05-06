from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import DateTime, Integer
from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


engine = create_async_engine(url='sqlite+aiosqlite:///db/db.sqlite3')
async_session = async_sessionmaker(engine)



class Base(DeclarativeBase):
    pass

class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)