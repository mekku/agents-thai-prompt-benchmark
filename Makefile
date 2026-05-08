RUNS  ?= 3
REPO  ?= $(shell pwd)
LABEL ?=

FLASK_DIR    := $(shell pwd)/bench/repos/flask
ELECTION_DIR := $(shell pwd)/bench/repos/election-live

.PHONY: setup bench bench-claude bench-all bench-flask bench-flask-claude bench-flask-all bench-election bench-election-claude bench-election-all summary clean setup-flask setup-election

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

setup-election:
	@if [ ! -d bench/repos/election-live ]; then \
	  mkdir -p bench/repos && \
	  git clone --depth=1 https://github.com/electinth/election-live bench/repos/election-live; \
	fi

bench-election: setup setup-election
	./bench/run-bench.sh $(RUNS) $(ELECTION_DIR) election

bench-election-claude: setup setup-election
	./bench/run-bench-claude.sh $(RUNS) $(ELECTION_DIR) election

bench-election-all: bench-election bench-election-claude

summary:
	./bench/summarize-results.py

clean:
	rm -rf bench/results
