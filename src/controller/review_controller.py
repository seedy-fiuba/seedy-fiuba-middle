from ..client import projects

async def requestReview(reviewerId: int, projectId: int):
    # Update project with status pendingReviewer
    project = await projects.updateProjectStatus(projectId, 'pending-reviewer')

    # Create review request in users TODO

    return {
        "reviewerId": reviewerId,
        "project": project
    }
