from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    input_channel: str = Field("input_channel", env="INPUT_CHANNEL")
    output_channel: str = Field("output_channel", env="OUTPUT_CHANNEL")
    redis_url: str = Field("redis://localhost:6379")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


if __name__ == "__main__":
    print(settings)
