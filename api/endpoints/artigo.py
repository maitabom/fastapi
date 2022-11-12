from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import Artigo

from core.deps import get_session, get_current_user

router = APIRouter()


@router.get('/', response_model=List[Artigo])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().unique().all()

        return artigos


@router.get('/{artigo_id}', response_model=Artigo, status_code=status.HTTP_200_OK)
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(detail='Artigo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Artigo)
async def post_artigo(artigo: Artigo, usuario: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    novo: Artigo = Artigo(
        titulo=artigo.titulo,
        descricao=artigo.descricao,
        url_fonte=artigo.url_fonte,
        usuario_id=artigo.usuario_id
    )

    db.add(novo)
    await db.commit()

    return novo


@router.put('/{artigo_id}', response_model=Artigo, status_code=status.HTTP_202_ACCEPTED)
async def put_artigo(artigo_id: int, artigo: Artigo, db: AsyncSession = Depends(get_session), usuario: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        entity: ArtigoModel = result.scalars().unique().one_or_none()

        if entity:
            if artigo.titulo:
                entity.titulo = artigo.titulo

            if artigo.descricao:
                entity.descricao = artigo.descricao

            if artigo.url_fonte:
                entity.url_fonte = artigo.url_fonte

            if usuario.id != entity.usuario_id:
                entity.usuario_id = usuario.id

            await session.commit

            return entity
        else:
            raise HTTPException(detail='Artigo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{artigo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def put_artigo(artigo_id: int, db: AsyncSession = Depends(get_session), usuario: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        marcado: ArtigoModel = result.scalars().unique().one_or_none()

        if marcado:
            await session.delete(marcado)
            await session.commit

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Artigo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)

