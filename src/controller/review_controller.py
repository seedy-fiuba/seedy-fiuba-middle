from ..client import projects
from ..client import users

async def requestReview(review):
    # Update project with status pendingReviewer
    project = await projects.updateProjectStatus(review.projectId, projects.Status.PENDING_REVIEWER)

    # Create review request in users
    review_request = await users.createReviewRequest(review)

    return {
        "review": review_request,
        "project": project
    }
