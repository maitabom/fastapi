from fastapi import APIRouter

from api.endpoints import artigo, usuario, curso

api_router = APIRouter()

api_router.include_router(artigo.router, prefix='/artigos', tags=['artigos'])
api_router.include_router(usuario.router, prefix='/usuarios', tags=['usuarios'])
#api_router.include_router(curso.router, prefix='/cursos', tags=['cursos'])
