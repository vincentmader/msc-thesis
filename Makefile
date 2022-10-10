all:
	make run_solver
	make plot_kernel

run_solver:
	./venv/bin/python3 ./src/main.py

plot_kernel:
	./venv/bin/python3 ./src/plot_kernel.py

setup:
	./bin/setup.sh

clean:
	rm ./data/*
	rm ./figures/*
