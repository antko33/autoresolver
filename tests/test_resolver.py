import os
from pathlib import Path

import pytest

from app.resolver import Resolver, save_to_file


@pytest.mark.asyncio
async def test_resolve_yt():
    resolved_ips = await __resolve()

    assert len(resolved_ips) > 0


@pytest.mark.asyncio
async def test_create_file():
    resolved_ips = await __resolve()
    filename = save_to_file(resolved_ips)

    file = Path(filename)
    assert file.exists()
    assert file.is_file()

    with open(filename, "r", encoding="utf-8") as f:
        content = f.readlines()
    assert len(content) > 0

    if file.exists():
        os.remove(filename)


async def __resolve() -> set[str]:
    dns_list = {"Google": ["8.8.8.8", "8.8.4.4"], "Yandex": ["77.88.8.8", "77.88.8.1"]}

    resolver = Resolver(dns_list, {"youtube_mini": ["youtube.com"]})
    result = await resolver.resolve_all()

    return result
