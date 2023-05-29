from pydantic import BaseSettings


# model to check environment variables
class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_hostname: str
    database_port: int
    database_name: str
    access_token_minute_expires: int
    algorithm: str
    secret_key: str
    
    class Config:
        env_file = '.env'

settings = Settings()
