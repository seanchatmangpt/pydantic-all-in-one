import os

from faststream import FastStream
from faststream.redis import RedisBroker, TestRedisBroker
from pydantic import BaseModel, Field, PositiveInt
from pyd4all.config import settings


def get_broker() -> RedisBroker:
    use_testbroker = os.getenv("USE_TESTBROKER", "false").lower() == "true"
    if use_testbroker:
        broker = TestRedisBroker(RedisBroker(settings.redis_url))
        print("Using TestRedisBroker (in-memory).")
    else:
        broker = RedisBroker(settings.redis_url)
        print("Using real Redis broker.")
    return broker


class User(BaseModel):
    user_id: PositiveInt = Field(...)
    user: str = Field(...)


def create_app() -> FastStream:
    broker = RedisBroker("redis://localhost:6379")
    app = FastStream(broker)

    @broker.subscriber(settings.input_channel)
    @broker.publisher(settings.output_channel)
    async def process_message(data: User) -> dict:
        """Process incoming messages and sends them to the output channel."""
        processed_message = {"message": f"User: {data.user_id} - {data.user} registered."}
        return processed_message

    return app
