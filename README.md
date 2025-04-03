# Loke

A prometheus exporter to monitor servers

## Setup

**Install venv**:
```bash
python3 -m venv .env
. ./.env/bin/activate
pip install -r req.txt
```
or
```bash
make install
```


**Start exporter**:
```bash
python ./src/main.py
```
or
```bash
make start
```

**Test**:

Now it should export data on port 8080. 8080 is the default port you can change it using the `-p` flag.
```bash
curl http://127.0.0.1:8080
```
