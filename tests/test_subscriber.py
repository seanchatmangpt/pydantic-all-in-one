import pytest
from pydantic import ValidationError

from faststream.redis import TestRedisBroker

from faststream import FastStream
from faststream.redis import RedisBroker

broker = RedisBroker("redis://localhost:6379")
app = FastStream(broker)


@broker.subscriber("test-channel")
async def handle(
    name: str,
    user_id: int,
):
    assert name == "John"
    assert user_id == 1

@pytest.mark.asyncio
async def test_handle():
    async with TestRedisBroker(broker) as br:
        await br.publish({"name": "John", "user_id": 1}, channel="test-channel")


@pytest.mark.asyncio
async def test_handle2():
    async with TestRedisBroker(broker) as br:
        await br.publish({"name": "John", "user_id": 1}, channel="test-channel")

        handle.mock.assert_called_once_with({"name": "John", "user_id": 1})
        

@pytest.mark.asyncio
async def test_handle3():
    async with TestRedisBroker(broker) as br:
        await br.publish({"name": "John", "user_id": 1}, channel="test-channel")

        handle.mock.assert_called_once_with({"name": "John", "user_id": 1})

    assert handle.mock is None