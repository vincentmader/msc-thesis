solver:
	./bin/run.sh
v1:
	./venv/bin/python3 ./src/coag_solvers/v01_py/src/main.py
v2:
	cd ./src/coag_solvers/v02_rs && cargo run --release
both:
	make v2
	make v1
setup:
	./bin/setup.sh
all:
	make setup
	make solver
