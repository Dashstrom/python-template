error:
	@echo "Please choose one of the following target: run, dev, completion, rerun, log, down"
	@exit 2

PHONY: run
run:
	docker-compose up -d

PHONY: dev
dev: rm
	docker-compose --file docker-compose.dev.yml up --build

PHONY: completion
completion:
	(cd backend && pip install -r requirements.dev.txt)
	(cd frontend && npm install)
	@echo 'All is done, enjoy coding'

PHONY: rerun
rerun:
	docker-compose up --build --force-recreate --no-deps -d

PHONY: log
logs:
	docker-compose logs -f

PHONY: down
rm:
	docker-compose stop
	docker-compose rm -f

PHONY: test
test:
	(cd backend && tox .)
