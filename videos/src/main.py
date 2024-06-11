from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .recomendations.router import recomendations_router
from .videos.router import tag_router
from .videos.router import video_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

app.include_router(tag_router)
app.include_router(video_router)
app.include_router(recomendations_router)
