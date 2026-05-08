RUNS  ?= 3
REPO  ?= $(shell pwd)
LABEL ?=

FLASK_DIR := $(shell pwd)/bench/repos/flask

.PHONY: setup bench bench-claude bench-all bench-flask bench-flask-claude bench-flask-all summary clean setup-flask

setup:
	chmod +x bench/*.sh bench/*.py

bench: setup
	./bench/run-bench.sh $(RUNS) $(REPO) $(LABEL)

bench-claude: setup
	./bench/run-bench-claude.sh $(RUNS) $(REPO) $(LABEL)

bench-all: bench bench-claude

setup-flask:
	@if [ ! -d bench/repos/flask ]; then \
	  mkdir -p bench/repos && \
	  git clone --depth=1 https://github.com/pallets/flask bench/repos/flask; \
	fi

bench-flask: setup setup-flask
	./bench/run-bench.sh $(RUNS) $(FLASK_DIR) flask

bench-flask-claude: setup setup-flask
	./bench/run-bench-claude.sh $(RUNS) $(FLASK_DIR) flask

bench-flask-all: bench-flask bench-flask-claude

summary:
	./bench/summarize-results.py

clean:
	rm -rf bench/results
