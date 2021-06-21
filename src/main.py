from fastapi import FastAPI
from .client.projects import *

app = FastAPI()
print("app is up!")


@app.get('/')
def helloWorld():
    return 'MiddleSeedyFiuba :)'


@app.post('/reviewer/{reviewerId}/project/{projectId}')
async def requestReviewerForProject(reviewerId: int, projectId: int):
    project = await getProject(projectId)
    return {
        "reviewerId": reviewerId,
        "project": project
    }
