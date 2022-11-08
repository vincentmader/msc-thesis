solver:
	clear
	./bin/run.sh
v1:
	clear
	./venv/bin/python3 ./src/coag_solvers/v01_py/src/main.py
v2:
	clear
	cd ./src/coag_solvers/v02_rs && cargo run --release
both:
	make v2
	make v1
setup:
	clear
	./bin/setup.sh
all:
	make setup
	make solver
rm:
	rm -r ./out/data/*
	rm -r ./out/figures/*
