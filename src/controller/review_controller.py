from ..client import projects as projects_client, users as users_client
from ..models import projects, users
from ..payloads import ReviewRequestPayload, ReviewUpdatePayload
from ..responses import ReviewResponseModel, ReviewProjectSearchResponse
import json


PROJECT_STATUS_FOR_REVIEW_STATUS = {
    users.ReviewStatus.approved: projects.Status.IN_PROGRESS,
    users.ReviewStatus.rejected: projects.Status.CREATED
}


async def request_review(review: ReviewRequestPayload):
    # Update project with status pendingReviewer
    project = await projects_client.update_project(review.projectId, {'status': projects.Status.PENDING_REVIEWER})

    # Create review request in users
    review_request = await users_client.create_review_request(review)


    return ReviewResponseModel(
        review=review_request,
        project=project
    )


async def update_review(reviewId: int, payload: ReviewUpdatePayload):
    # Update review status
    review = await users_client.update_review_request(reviewId, payload.status)
    print(review)
    # Update project status
    project = await projects_client.update_project(review.projectId,
                                                   {
                                                       'status': PROJECT_STATUS_FOR_REVIEW_STATUS[payload.status],
                                                       'reviewerId': review.reviewerId
                                                   })

    return ReviewResponseModel(
        review=review,
        project=project
    )


async def get_reviews(reviewer_id: str, status: str):
    params = {}

    if reviewer_id is not None:
        params['reviewerId'] = reviewer_id

    if status is not None:
        params['status'] = status

    reviews = await users_client.search_review_request(params)

    projects_ids = list(map(lambda r: str(r.projectId), reviews.results))
    projects_results = await projects_client.search_project({'id': ",".join(projects_ids)})

    search_results = []

    for review in reviews.results:
        project = list(filter(lambda p: p.id == review.projectId, projects_results.results))
        if len(project) > 0:
            project = project[0]
        else:
            project = None

        result = ReviewResponseModel(review=review, project=project)
        search_results.append(result)

    return ReviewProjectSearchResponse(size=reviews.size, results=search_results)
