from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .users import auth_router
from .users import user_router

app = FastAPI(title="YouTube Users")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

app.include_router(auth_router)
app.include_router(user_router)
