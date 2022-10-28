import requests
import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.shortener_url.models import Url


@pytest.mark.asyncio
async def test_create_url(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    payload = test_data["case_create"]["payload"]

    response = await async_client.post("/shorten_url", json=payload)

    assert response.status_code == 201

    got = response.json()

    key = got["shortened_url"].split("/")[-1]

    assert key.isalnum() is True
    assert len(key) == 8


@pytest.mark.asyncio
async def test_create_url_fail(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    payload_fail = test_data["case_create"]["fail_payload"]
    response = await async_client.post("shorten_url", json=payload_fail)

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

    response = await async_client.get(f"/{url_data['key']}")

    assert response.status_code == 301
    # Get redirect url from httpx response
    redirect_url = response.next_request.url

    want = test_data["case_get"]["want"]

    assert redirect_url == want["url"]


@pytest.mark.asyncio
async def test_get_url_fail(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    url_data = test_data["initial_data"]["url"]
    statement = insert(Url).values(url_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    failed_key = test_data["case_get"]["fail_payload"]

    response = await async_client.get(f"/{failed_key}")

    assert response.status_code == 404

    got = response.json()
    want_fail = test_data["case_get"]["fail_want"]

    for key, value in want_fail.items():
        assert got[key] == value


@pytest.mark.asyncio
async def test_get_count_null(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):

    response = await async_client.get("/count")

    assert response.status_code == 200
    assert response.json() == {"Calls": 0}


@pytest.mark.asyncio
async def test_get_count_1(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    url_data = test_data["initial_data"]["url"]
    statement = insert(Url).values(url_data)
    await async_session.execute(statement=statement)
    await async_session.commit()
    response = await async_client.get("/count")

    assert response.status_code == 200
    assert response.json() == {"Calls": 1}


@pytest.mark.asyncio
async def test_get_count_2_with_2_diff_urls(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    payloads = test_data["case_count_2_diff_urls"]["payloads"]
    for payload in payloads:
        statement = insert(Url).values(payload)
        await async_session.execute(statement=statement)
        await async_session.commit()

    response = await async_client.get("/count")
    want = test_data["case_count_2_diff_urls"]["want"]

    assert response.status_code == 200
    assert response.json() == want


@pytest.mark.asyncio
async def test_get_count_2_with_2_diff_users(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):

    payload = test_data["case_count_2_diff_users"]["payload"]
    statement = insert(Url).values(payload)
    await async_session.execute(statement=statement)
    await async_session.commit()

    new_user_data = test_data["case_count_2_diff_users"]["new_user_data"]
    await async_client.post("shorten_url", json=new_user_data)

    response = await async_client.get("/count")
    want = test_data["case_count_2_diff_users"]["want"]

    assert response.status_code == 200
    assert response.json() == want


@pytest.mark.asyncio
async def test_get_top_10_null(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get("/top_10")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_top_10_null(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.get("/top_10")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_top_10_one_record(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    url_data = test_data["initial_data"]["url"]
    statement = insert(Url).values(url_data)
    await async_session.execute(statement=statement)
    await async_session.commit()
    response = await async_client.get("/top_10")

    want = test_data["case_get_top_10_1"]["want"]
    assert response.status_code == 200
    assert response.json() == want


@pytest.mark.asyncio
async def test_get_top_10_ten_records(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    payloads = test_data["case_get_top_10_ten_records"]["payloads"]
    for payload in payloads:
        statement = insert(Url).values(payload)
        await async_session.execute(statement=statement)
        await async_session.commit()

    response = await async_client.get("/top_10")

    want = test_data["case_get_top_10_ten_records"]["want"]
    assert response.status_code == 200
    assert response.json() == want
