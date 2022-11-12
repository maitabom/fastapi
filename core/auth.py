import json
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import EmailStr
from pytz import timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.configs import settings
from core.security import verify_password
from models.usuario_model import UsuarioModel

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_STR}/usuarios/login'
)


async def authenticate(email: EmailStr, password: str, db: AsyncSession) -> Optional[UsuarioModel]:
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if not usuario:
            return None

        if not verify_password(password, usuario.senha):
            return None

        return usuario


def create_token(type: str, timeout: timedelta, sub: str) -> str:
    payload = {}

    tz = timezone('America/Sao_Paulo')
    expire = datetime.now(tz=tz) + timeout

    payload['type'] = type
    payload['exp'] = expire.timestamp()
    payload['iap'] = datetime.now(tz=tz).timestamp()
    payload['sub'] = str(sub)

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

    return token


def create_token_access(sub: str) -> str:
    return create_token(
        type='access_token',
        timeout=timedelta(settings.ACCESS_EXPIRE_MINUTES),
        sub=sub
    )


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)