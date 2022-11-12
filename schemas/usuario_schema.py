from typing import Optional, List
from pydantic import BaseModel, EmailStr

from schemas.artigo_schema import Artigo


class Usuario(BaseModel):
    id: Optional[int]
    nome: str
    sobrenome: str
    email: EmailStr
    administrador: bool = False

    class Config:
        orm_mode = True


class UsuarioCreate(Usuario):
    senha: str


class UsuarioUpdate(Usuario):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    administrador: Optional[bool] = False


class UsuarioArtigos(Usuario):
    artigos: Optional[List[Artigo]]
