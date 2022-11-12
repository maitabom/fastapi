from typing import List
from unittest import result
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import CursoModel
from schemas.curso_schema import Curso
from core.deps import get_session

router = APIRouter()

@router.get('/', response_model=List[Curso])
async def get_curso(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()
        
        return cursos


@router.get('/{curso_id}', response_model=Curso, status_code=status.HTTP_200_OK)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()

        if curso:
            return curso
        else:
            raise HTTPException(detail='Curso não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Curso)
async def post_curso(curso: Curso, db: AsyncSession = Depends(get_session)):
    novo_curso = Curso(
        titulo=curso.titulo, 
        aulas=curso.aulas,
        horas=curso.horas
    )

    db.add(novo_curso)
    await db.commit()

    return novo_curso

@router.put('/{curso_id}', response_model=Curso, status_code=status.HTTP_202_ACCEPTED)
async def put_curso(curso_id: int, curso: Curso, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(Curso.id == curso_id)
        result = await session.execute(query)
        pivot = result.scalar_one_or_none()

        if pivot:
            pivot.titulo = curso.titulo
            pivot.aulas = curso.aulas
            pivot.horas = curso.horas

            await session.commit()

            return pivot
        else:
            raise HTTPException(detail='Curso não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        marcado = result.scalar_one_or_none()

        if marcado:
            await session.delete(marcado)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Curso não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
