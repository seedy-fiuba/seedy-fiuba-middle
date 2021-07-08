from fastapi import FastAPI, Request
from .controller import review_controller, projects_controller, wallet_controller
from dotenv import load_dotenv
from .responses import ReviewResponseModel, ReviewProjectSearchResponse, WalletBalanceResponse
from .payloads import ReviewRequestPayload, ReviewUpdatePayload, FundProjectPayload, AcceptStagePayload
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


# REVIEWS: TODO: Armar router para reviews
@app.post('/reviews', response_model=ReviewResponseModel, status_code=201)
async def request_reviewer_for_project(review: ReviewRequestPayload):
    return await review_controller.request_review(review)


@app.put('/reviews/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, payload: ReviewUpdatePayload):
    return await review_controller.update_review(review_id, payload)


@app.get('/reviews', response_model=ReviewProjectSearchResponse)
async def get_reviews(reviewerId: Optional[str] = None, status: Optional[str] = None):
    return await review_controller.get_reviews(reviewerId, status)


# PROJECTS: TODO: Armar router para projects
@app.post('/projects/{project_id}/fund')
async def fund_project(project_id: int, payload: FundProjectPayload):
    return await projects_controller.fund_project(project_id, payload)


@app.post('/projects/{project_id}/stages/{stage_id}/accept')
async def accept_stage(project_id: int, stage_id: int, payload: AcceptStagePayload):
    return await projects_controller.accept_stage(project_id, stage_id, payload)


# WALLET
@app.get('/wallet/{user_id}', response_model=WalletBalanceResponse)
async def get_wallet_balance(user_id: int):
    return await wallet_controller.get_balance(user_id)
