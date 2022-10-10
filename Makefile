all:
	make run_solver

run_solver:
	./venv/bin/python3 ./src/main.py

setup:
	./bin/setup.sh

clean:
	rm -r ./data/*
	rm -r ./figures/*
