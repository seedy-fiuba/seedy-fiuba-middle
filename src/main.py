from fastapi import FastAPI
from .client.projects import *
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

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
