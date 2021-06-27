from ..client import projects
from ..client import users


async def request_review(review):
    # Update project with status pendingReviewer
    project = await projects.update_project_status(review.projectId, projects.Status.PENDING_REVIEWER)

    # Create review request in users
    review_request = await users.create_review_request(review)

    return {
        "review": review_request,
        "project": project
    }
