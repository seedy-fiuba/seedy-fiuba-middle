from fastapi import FastAPI, Depends
from .controller import review_controller
from dotenv import load_dotenv
from .router import projects
from .dependencies import getTokenHeader

load_dotenv()  # take environment variables from .env.

app = FastAPI(dependencies=[Depends(getTokenHeader)])
app.include_router(projects.router)

print("app is up!")


@app.get('/')
def helloWorld():
    return 'MiddleSeedyFiuba :)'


@app.post('/reviewer/{reviewerId}/project/{projectId}')
async def requestReviewerForProject(reviewerId: int, projectId: int):
    data = await review_controller.requestReview(reviewerId, projectId)
    return data
