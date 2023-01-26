all:
	docker-compose -f docker-compose.dev.yml build api
	docker-compose -f docker-compose.dev.yml up api
down:
	docker-compose -f docker-compose.dev.yml down
api:
	docker-compose -f docker-compose.dev.yml build api
	docker-compose -f docker-compose.dev.yml up api
app:
	docker-compose -f docker-compose.dev.yml build app
	docker-compose -f docker-compose.dev.yml up app
db:
	docker-compose -f docker-compose.dev.yml build mysql_db
	docker-compose -f docker-compose.dev.yml up -d mysql_db
db-prod:
	docker-compose -f docker-compose.prod.yml build mysql_db
	docker-compose -f docker-compose.prod.yml up -d mysql_db