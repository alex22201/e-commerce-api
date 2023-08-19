from typing import List

from tortoise.signals import post_save

from src.models import Business, User, business_pydantic


@post_save(User)
async def create_business(
        sender: 'Type[User]', # noqa
        instance: User,
        created: bool,
        using_db: 'Optional[BaseDBAsyncClient]', # noqa
        update_fields: List[str] # noqa
) -> None:
    if created:
        business_obj: Business = await Business.create(
            name=instance.username,
            owner=instance
        )
        await business_pydantic.from_tortoise_orm(business_obj)
