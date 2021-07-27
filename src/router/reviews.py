from fastapi import APIRouter, status as HTTPStatus
from ..controller import review_controller
from src.responses import ReviewResponseModel, ReviewProjectSearchResponse
from src.payloads import ReviewRequestPayload, ReviewUpdatePayload
from typing import Optional

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)


@router.post('', response_model=ReviewResponseModel, status_code=HTTPStatus.HTTP_201_CREATED)
async def request_reviewer_for_project(review: ReviewRequestPayload):
    return await review_controller.request_review(review)


@router.put('/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, payload: ReviewUpdatePayload):
    return await review_controller.update_review(review_id, payload)


@router.get('', response_model=ReviewProjectSearchResponse)
async def get_reviews(reviewerId: Optional[str] = None, status: Optional[str] = None):
    return await review_controller.get_reviews(reviewerId, status)


