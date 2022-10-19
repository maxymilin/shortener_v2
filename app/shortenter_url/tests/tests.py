import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.shortenter_url.models import Url


@pytest.mark.asyncio
async def test_create_url(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    payload = test_data["case_create"]["payload"]

    response = await async_client.post("/url", json=payload)

    assert response.status_code == 201

    got = response.json()
    want = test_data["case_create"]["want"]

    for key, value in want.items():
        assert got[key] == value


@pytest.mark.asyncio
async def test_create_url_fail(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    payload_fail = test_data["case_create"]["fail_payload"]
    response = await async_client.post("/url", json=payload_fail)

    assert response.status_code == 400

    got = response.json()
    want_fail = test_data["case_create"]["fail_want"]

    for key, value in want_fail.items():
        assert got[key] == value


@pytest.mark.asyncio
async def test_get_url(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    url_data = test_data["initial_data"]["url"]
    statement = insert(Url).values(url_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    response = await async_client.get(f"/url/{url_data['key']}")

    assert response.status_code == 200

    got = response.json()

    want = test_data["case_get"]["want"]

    for key, value in want.items():
        assert got[key] == value


@pytest.mark.asyncio
async def test_get_url_fail(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    url_data = test_data["initial_data"]["url"]
    statement = insert(Url).values(url_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    failed_key = test_data["case_get"]["fail_payload"]

    response = await async_client.get(f"/url/{failed_key}")

    assert response.status_code == 404

    got = response.json()
    want_fail = test_data["case_get"]["fail_want"]

    for key, value in want_fail.items():
        assert got[key] == value
