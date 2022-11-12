from typing import List
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from jose.constants import ALGORITHMS

class Settings(BaseSettings):
    API_STR: str = '/api'
    DB_URL:str = 'postgresql+asyncpg://developer:123456@localhost:5432/faculdade' 
    DBBaseModel = declarative_base()
    JWT_SECRET: str = 'kwlvSGlSUzyF9CbZA6psD2ZmR-EoOYGeSMSBNJT0vxQ'
    ALGORITHM: str = ALGORITHMS.HS256
    ACCESS_EXPIRE_MINUTES: int = (60 * 24 * 7)

    class Config:
        case_sensitive = True


settings: Settings = Settings()