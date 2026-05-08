RUNS ?= 3

.PHONY: setup bench summary clean

setup:
	chmod +x bench/*.sh bench/*.py

bench: setup
	./bench/run-bench.sh $(RUNS)

summary:
	./bench/summarize-results.py

clean:
	rm -rf bench/results
