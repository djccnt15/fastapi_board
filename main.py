from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from settings.config import get_config, mode
from settings.routes import router

app = FastAPI()

origins = get_config()['CORSLIST'].get(mode).split()  # get CORS allow list

app.add_middleware(  # allow CORS credential
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(router)


@app.get("/")
def index():
    return {"message": "This is temporal index page"}


@app.get("/hello")
def hello():
    return {"message": "Hello World!"}