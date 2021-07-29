from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.router import projects as projects_router, reviews as reviews_router, \
    wallet as wallet_router, users as users_router, contracts as contracts_router, \
    servers as servers_router, auth as auth_router
from dotenv import load_dotenv
from src import exceptions
from fastapi.responses import JSONResponse

load_dotenv()  # take environment variables from .env.

app = FastAPI()
print("app is up!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.exception_handler(exceptions.MiddleException)
async def unicorn_exception_handler(request: Request, exc: exceptions.MiddleException):
    return JSONResponse(
        status_code=exc.status[0],
        content=exc.detail,
    )

app.include_router(projects_router.router)
app.include_router(users_router.router)
app.include_router(auth_router.router)
app.include_router(reviews_router.router)
app.include_router(wallet_router.router)
app.include_router(contracts_router.router)
app.include_router(servers_router.router)


@app.get('/')
def hello_world():
    return 'MiddleSeedyFiuba :)'

