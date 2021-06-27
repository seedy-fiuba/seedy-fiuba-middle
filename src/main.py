from fastapi import FastAPI
from .controller import review_controller
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()  # take environment variables from .env.

app = FastAPI()
print("app is up!")


class ReviewRequest(BaseModel):
    reviewerId: int
    projectId: int


@app.get('/')
def helloWorld():
    return 'MiddleSeedyFiuba :)'


@app.post('/reviews')
async def requestReviewerForProject(review: ReviewRequest):
    data = await review_controller.requestReview(review)
    return data
