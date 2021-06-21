FROM python:3.7

WORKDIR /usr/src/app

# Install app dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Bundle app source
COPY . .

# Bare in mind, expose is not supported by heroku. This is only for local testing.
EXPOSE $PORT

CMD uvicorn src.main:app --host 0.0.0.0 --port $PORT