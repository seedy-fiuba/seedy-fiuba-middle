from ..models import projects, users
from ..client.responses.smart_contract import ProjectStatus


PROJECT_STATUS_FOR_REVIEW_STATUS = {
    users.ReviewStatus.approved: projects.Status.FUNDING,
    users.ReviewStatus.rejected: projects.Status.CREATED
}


PROJECT_STATUS_FOR_SC_STATUS = {
    ProjectStatus.FUNDING: projects.Status.FUNDING,
    ProjectStatus.IN_PROGRESS: projects.Status.IN_PROGRESS,
    ProjectStatus.COMPLETED: projects.Status.COMPLETED
}