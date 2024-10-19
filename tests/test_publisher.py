import pytest
from pydantic import ValidationError

from faststream.redis import TestRedisBroker

from faststream import FastStream
from faststream.redis import RedisBroker

broker = RedisBroker("redis://localhost:6379")
app = FastStream(broker)


publisher = broker.publisher("another-channel")

@publisher
@broker.subscriber("test-channel")
async def handle() -> str:
    return "Hi!"


import pytest

from faststream.redis import TestRedisBroker

@pytest.mark.asyncio
async def test_handle():
    async with TestRedisBroker(broker) as br:
        await br.publish("", channel="test-channel")
        publisher.mock.assert_called_once_with("Hi!")