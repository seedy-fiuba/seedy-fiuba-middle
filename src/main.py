from fastapi import FastAPI, Request
from src.controller import review_controller, projects_controller, wallet_controller
from dotenv import load_dotenv
from src.responses import ReviewResponseModel, ReviewProjectSearchResponse, WalletBalanceResponse
from src.payloads import ReviewRequestPayload, ReviewUpdatePayload, FundProjectPayload, AcceptStagePayload, \
    TransferFundsPayload
from src import exceptions
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi import status
from typing import Optional

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


# REVIEWS
@app.post('/reviews', response_model=ReviewResponseModel, status_code=status.HTTP_201_CREATED, tags=['reviews'])
async def request_reviewer_for_project(review: ReviewRequestPayload):
    return await review_controller.request_review(review)


@app.put('/reviews/{review_id}', response_model=ReviewResponseModel, tags=['reviews'])
async def update_review(review_id: int, payload: ReviewUpdatePayload):
    return await review_controller.update_review(review_id, payload)


@app.get('/reviews', response_model=ReviewProjectSearchResponse, tags=['reviews'])
async def get_reviews(reviewerId: Optional[str] = None, status: Optional[str] = None):
    return await review_controller.get_reviews(reviewerId, status)


# PROJECTS
@app.post('/projects/{project_id}/fund', tags=['projects'], response_class=PlainTextResponse)
async def fund_project(project_id: int, payload: FundProjectPayload):
    return await projects_controller.fund_project(project_id, payload)


@app.post('/projects/{project_id}/stages/{stage_id}/accept', tags=['projects'], response_class=PlainTextResponse)
async def accept_stage(project_id: int, stage_id: int, payload: AcceptStagePayload):
    return await projects_controller.accept_stage(project_id, stage_id, payload)


@app.post('/projects/{project_id}/review', tags=['projects'])
async def request_stage_review(project_id: int):
    return await projects_controller.request_stage_review(project_id)


# WALLET
@app.get('/wallet/{user_id}', response_model=WalletBalanceResponse, tags=['wallet'])
async def get_wallet_balance(user_id: int):
    return await wallet_controller.get_balance(user_id)


@app.post('/wallet/{user_id}/transfer', status_code=status.HTTP_204_NO_CONTENT, response_class=PlainTextResponse,
          tags=['wallet'])
async def transfer_funds(user_id: int, payload: TransferFundsPayload):
    return await wallet_controller.transfer_funds(user_id, payload)
