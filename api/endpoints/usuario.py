from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import Usuario, UsuarioArtigos, UsuarioCreate, UsuarioUpdate
from core.deps import get_session, get_current_user
from core.security import make_hash_password
from core.auth import authenticate, create_token_access

router = APIRouter()


@router.get('/authenticate', response_model=Usuario)
def get_authenticate(usuario: UsuarioModel = Depends(get_current_user)):
    return usuario


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=Usuario)
async def post_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_session)):
    new_user: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        administrador=usuario.administrador,
        senha=make_hash_password(usuario.senha)
    )

    async with db as session:
        try:
            session.add(new_user)
            await session.commit()
            return new_user
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Já existe um usuário com este e-mail cadastrado')

        
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await authenticate(email=form_data.username, password=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos')

    return JSONResponse(content={
        'access_token': create_token_access(sub=usuario.id),
        'token_type': 'bearer'
    }, status_code=status.HTTP_200_OK)


@router.get('/', response_model=List[Usuario])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[Usuario] = result.scalars().unique().all()

        return usuarios


@router.get('/{usuario_id}', response_model=UsuarioArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioArtigos = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{usuario_id}', response_model=Usuario, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        entity: Usuario = result.scalars().unique().one_or_none()

        if entity:
            if usuario.nome:
                entity.nome = usuario.nome

            if usuario.sobrenome:
                entity.sobrenome = usuario.sobrenome

            if usuario.email:
                entity.email = usuario.email

            if usuario.administrador:
                entity.administrador = usuario.administrador

            if usuario.senha:
                entity.senha = make_hash_password(usuario.senha)

            await session.commit()

            return entity
        else:
            raise HTTPException(detail='Usuário não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioArtigos = result.scalars().unique().one_or_none()

        if usuario:
            await session.delete(usuario)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usuário não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
