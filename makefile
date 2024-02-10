save:
	git add --all
	git commit -m "Unnamed Progress :writting_hand:"
	git push origin HEAD

t:
	make t-crud

t-crud:
	pytest test_crud.py -s

t-end:
	pytest test_util_endpoints.py -s

saven:
	git add --all
	git commit -m "${m}"
	git push origin HEAD

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv test_main.py

format:
	black *.py

run:
	python main.py

run-uvicorn:
	uvicorn main:app --reload

killweb:
	sudo killall uvicorn

lint:
	pylint --disable=R,C main.py

all: install lint

env:
	env\Scripts\activate

forceinstall:
	pip install --upgrade --force-reinstall -r requirements.txt

deploy:
	git checkout deployment
	git merge main
	git push origin HEAD
	git checkout main
	
docker:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 796522278827.dkr.ecr.us-east-1.amazonaws.com
	docker build -t fastapi-plat-v2 .
	docker tag fastapi-plat-v2:latest 796522278827.dkr.ecr.us-east-1.amazonaws.com/fastapi-plat-v2:latest
	docker push 796522278827.dkr.ecr.us-east-1.amazonaws.com/fastapi-plat-v2:latest

alembic-migrate:
	alembic revision --autogenerate -m "${m}"
	alembic upgrade head

alembic-reset:
	alembic stamp head


docker-clean:
	docker prune < y
