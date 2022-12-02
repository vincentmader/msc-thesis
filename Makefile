# ─────────────────────────────────────────────────────────────────────────────
solver:
	clear
	cd ./bin && ./run.sh
setup:
	clear
	cd ./bin && ./setup.sh
# ─────────────────────────────────────────────────────────────────────────────
v1:
	clear
	./venv/bin/python3 ./src/coag_solvers/v01_py/src/main.py
v2:
	clear
	cd ./src/coag_solvers/v02_rs && cargo run --release
both:
	make v2
	make v1
# ─────────────────────────────────────────────────────────────────────────────
test:
	clear
	./venv/bin/python3 ./src/coag_solvers/v01_py/src/tests.py

all:
	make setup
	make solver
# ─────────────────────────────────────────────────────────────────────────────
clean:
	rm -r ./venv
recompile:
	rm -r **/__pycache__
# ─────────────────────────────────────────────────────────────────────────────
