install:
	@if [ ! -d ".env" ]; then \
		python3 -m venv ".env"; \
	fi
	./.env/bin/pip install -r req.txt

start:
	./.env/bin/python ./src/main.py
