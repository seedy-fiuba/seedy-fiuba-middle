from fastapi import FastAPI, Request
from .controller import review_controller
from dotenv import load_dotenv
from pydantic import BaseModel
from .client import projects
from .client import users
from src import exceptions
from fastapi.responses import JSONResponse

load_dotenv()  # take environment variables from .env.

app = FastAPI()
print("app is up!")


class ReviewRequest(BaseModel):
    reviewerId: int
    projectId: int


class ReviewResponseModel(BaseModel):
    project: projects.Project
    review: users.Review


@app.exception_handler(exceptions.MiddleException)
async def unicorn_exception_handler(request: Request, exc: exceptions.MiddleException):
    return JSONResponse(
        status_code=exc.status[0],
        content=exc.detail,
    )


@app.get('/')
def hello_world():
    return 'MiddleSeedyFiuba :)'


@app.post('/reviews', response_model=ReviewResponseModel, status_code=201)
async def request_reviewer_for_project(review: ReviewRequest):
    data = await review_controller.request_review(review)
    return data
