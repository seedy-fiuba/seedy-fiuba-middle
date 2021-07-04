from fastapi import FastAPI, Request
from .controller import review_controller
from dotenv import load_dotenv
from .responses import ReviewResponseModel, ReviewProjectSearchResponse
from .payloads import ReviewRequestPayload, ReviewUpdatePayload
from src import exceptions
from fastapi.responses import JSONResponse
from typing import List, Optional

load_dotenv()  # take environment variables from .env.

app = FastAPI()
print("app is up!")


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
async def request_reviewer_for_project(review: ReviewRequestPayload):
    return await review_controller.request_review(review)


@app.put('/reviews/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, payload: ReviewUpdatePayload):
    return await review_controller.update_review(review_id, payload)


@app.get('/reviews', response_model=ReviewProjectSearchResponse)
async def get_reviews(reviewer_id: Optional[str] = None, status: Optional[str] = None):
    return await review_controller.get_reviews(reviewer_id, status)

