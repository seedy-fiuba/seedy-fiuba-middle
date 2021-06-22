from fastapi import FastAPI
from .controller import review_controller
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

app = FastAPI()
print("app is up!")


@app.get('/')
def helloWorld():
    return 'MiddleSeedyFiuba :)'


@app.post('/reviewer/{reviewerId}/project/{projectId}')
async def requestReviewerForProject(reviewerId: int, projectId: int):
    print(f"Will request reviewer {reviewerId} for project {projectId}")
    data = await review_controller.requestReview(reviewerId, projectId)
    return data
