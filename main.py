from configparser import ConfigParser

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

config = ConfigParser()
config.read('config.ini')
mode = config['DEFAULT'].get('mode')

app = FastAPI()

origins = config['CORSLIST'].get(mode).split()  # get CORS allow list from 'config.ini'

app.add_middleware(  # allow CORS credential
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "This is temporal index page"}


@app.get("/hello")
def hello():
    return {"message": "Hello World!"}