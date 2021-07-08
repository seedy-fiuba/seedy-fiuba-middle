from ..client import projects as projects_client, users as users_client, smart_contract as sc_client
from ..models import projects, users
from ..client.payloads.smart_contract import CreateSCProject
from ..client.payloads.projects import UpdateProjectPayload
from ..client.responses.smart_contract import ProjectStatus
from ..payloads import ReviewRequestPayload, ReviewUpdatePayload
from ..responses import ReviewResponseModel, ReviewProjectSearchResponse
from ..exceptions import MiddleException


PROJECT_STATUS_FOR_REVIEW_STATUS = {
    users.ReviewStatus.approved: projects.Status.FUNDING,
    users.ReviewStatus.rejected: projects.Status.CREATED
}

PROJECT_STATUS_FOR_SC_STATUS = {
    ProjectStatus.FUNDING: projects.Status.FUNDING,
    ProjectStatus.IN_PROGRESS: projects.Status.IN_PROGRESS,
    ProjectStatus.COMPLETED: projects.Status.COMPLETED
}


async def request_review(review: ReviewRequestPayload):
    # Update project with status pendingReviewer
    project = await projects_client.update_project(review.projectId,
                                                   UpdateProjectPayload(status=projects.Status.PENDING_REVIEWER))

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

    if payload.status == users.ReviewStatus.approved:
        # Get project
        project = await projects_client.get_project(review.projectId)

        # Get private keys for owner and reviewer
        owner = await users_client.get_user(project.ownerId)
        reviewer = await users_client.get_user(review.reviewerId)
        print(f"owner: {owner}")
        print(f"reviewer: {reviewer}")

        if owner.walletPrivateKey is None:
            raise MiddleException(status=400, detail={'error': 'Project Owner does not have a wallet', 'status': 400})

        if reviewer.walletPrivateKey is None:
            raise MiddleException(status=400, detail={'error': 'Project Owner does not have a wallet', 'status': 400})

        stages_cost = list(map(lambda stage: stage.targetAmount, project.stages))
        print(f"stages: {stages_cost}")

        # Create project in smart contract
        sc_project = await sc_client.create_project(
            CreateSCProject(
                ownerPrivateKey=owner.walletPrivateKey,
                reviewerPrivateKey=reviewer.walletPrivateKey,
                stagesCost=stages_cost
            ))
        print(f"sc_project: {str(vars(sc_project))}")

        project_update_payload = UpdateProjectPayload(
            status=PROJECT_STATUS_FOR_SC_STATUS[sc_project.projectStatus],
            currentStageId=sc_project.currentStage,
            walletId=sc_project.projectWalletId,
            reviewerId=review.reviewerId
        )
    else:
        project_update_payload = UpdateProjectPayload(
            status=PROJECT_STATUS_FOR_REVIEW_STATUS[payload.status],
            reviewerId=review.reviewerId
        )

    # Update project status
    project = await projects_client.update_project(review.projectId, project_update_payload)

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

    if reviews.size == 0:
        return ReviewProjectSearchResponse(size=reviews.size, results=[])

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
