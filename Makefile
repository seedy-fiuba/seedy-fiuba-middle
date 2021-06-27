run:
	docker-compose up --build

rundocker:
	docker compose up --build

clean:
	docker stop middle-api
	docker rm  middle-api

deploy:
	heroku container:login
	heroku container:push web --app seedy-fiuba-middle-api
	heroku container:release web --app seedy-fiuba-middle-api