from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from buildbox_challenge_final.database import engine, Base
from buildbox_challenge_final.routers import movies
from buildbox_challenge_final.logger import logger

app = FastAPI(title="IMDb Movie Tracker API", version="1.0")

app.mount("/static", StaticFiles(directory="buildbox_challenge_final/static"), name="static")

# Middleware para logar requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Recebida requisição {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Resposta {response.status_code} para {request.method} {request.url}")
    return response

# Criação async das tabelas
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(movies.router)

templates = Jinja2Templates(directory="buildbox_challenge_final/templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
