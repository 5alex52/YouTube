from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError


class ApiSettings(BaseSettings):
    S3_BUCKET_NAME: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_REGION: str
    S3_URL: str

    model_config = SettingsConfigDict(env_file=".env")

    @classmethod
    def validate_env(cls):
        try:
            cls()
        except ValidationError as e:
            error_details = e.errors()
            missing_parameters = [error["loc"][0] for error in error_details]
            if missing_parameters:
                raise ValueError(f"Missing parameters in .env file: {', '.join(missing_parameters)}")

ApiSettings().validate_env()
settings = ApiSettings()