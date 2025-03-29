import pytest

from app import models
from app.db import db_init
from app.models import Domain, User


@pytest.fixture(autouse=True)  # type: ignore[misc]
async def init_and_reset_db() -> None:
    await db_init()
    await __clear_all_data()


@pytest.mark.asyncio  # type: ignore[misc]
async def test_create_user_and_domain() -> None:
    user, created = await User.get_or_create(tg_id="123456")
    domain = await Domain.create(user=user, domain="test.com")

    assert domain.domain == "test.com"
    assert domain.user.id == user.id

    await user.fetch_related("domains")
    assert domain in user.domains
    assert len(user.domains) == 1


async def __clear_all_data() -> None:
    await models.User.all().delete()
    await models.Domain.all().delete()
    await models.Resolve.all().delete()
    await models.RoutingFile.all().delete()
