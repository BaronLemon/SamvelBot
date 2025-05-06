from datetime import datetime
from sqlalchemy.future import select
from db.models import Subscription, async_session


# add user to db or update sub time
async def add_or_update_subscription(user_id: int, expires_at: datetime):
    async with async_session() as session:
        result = await session.execute(select(Subscription).where(Subscription.user_id == user_id))
        sub = result.scalar_one_or_none()

        if sub:
            sub.expires_at = expires_at
        else:
            sub = Subscription(user_id=user_id, expires_at=expires_at)
            session.add(sub)

        await session.commit()

# get all users from db
async def get_all_subscriptions():
    async with async_session() as session:
        result = await session.execute(select(Subscription))
        return result.scalars().all()


# delete user when sub ends
async def remove_user(user_id: int):
    async with async_session() as session:
        result = await session.execute(select(Subscription).where(Subscription.user_id == user_id))
        sub = result.scalar_one_or_none()
        if sub:
            await session.delete(sub)
            await session.commit()
