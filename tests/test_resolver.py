import pytest

from app.resolver import Resolver


@pytest.mark.asyncio
async def test_resolve_yt():
    dns_list = dict()
    dns_list["Google"] = ["8.8.8.8", "8.8.4.4"]
    dns_list["Yandex"] = ["77.88.8.8", "77.88.8.1"]

    resolver = Resolver(dns_list, ["youtube.com"])
    result = await resolver.resolve_all()

    assert len(result) > 0
