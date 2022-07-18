from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname = "localhost"
    database_name = "fastapi"
    database_username = "postgres"
    database_password = "Shalini!1"
    database_port = "5432"
    secret_key = "thisisthefirsttimeamusingJWTforgeneratingthetokenanditsinteresting"
    algorithm = "HS256"
    access_token_expire_minutes = 120

    # class Config:
    #     env_file = ".env"


settings = Settings()
