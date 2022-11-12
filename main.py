import uvicorn
from fastapi import FastAPI

from api.api import api_router
from core.configs import settings

app = FastAPI(title='Curso de API com sergurança')

app.include_router(api_router, prefix=settings.API_STR)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)
    