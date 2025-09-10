.PHONY: test
test:venv
	python -m unittest discover -s tests 

.PHONY: venv
venv:
	. .venv/bin/activate

.PHONY:dev
dev: venv	
	flask --app webserver run --debug --extra-files ./templates/*:./static/*

