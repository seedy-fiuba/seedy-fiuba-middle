from fastapi import FastAPI

app = FastAPI()
print("app is up!")


@app.get('/')
def helloWorld():
    return 'MiddleSeedyFiuba :)'

