from pydantic_settings import BaseSettings #to perform validation/overriding our env vars

class Settings(BaseSettings): #to make sure that all these env vars are properly set
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = {
        "env_file": ".env"
    }


settings = Settings() #type: ignore
