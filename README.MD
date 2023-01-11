# Raspodijeljeni Sustavi - Projekt 1

## Setup

1. Instalirati pakete:

```sh
pip install -r requirements.txt
```

2. [Fake dataset JSON datoteka](https://huggingface.co/datasets/codeparrot/codeparrot-clean/resolve/main/file-000000000040.json.gz) (1 GB) mora biti `./podaci.json`

3. Pokrenuti sve servise:

```sh
python servis0.py
python servis1.py
.
.
.
```

4. GET request na servis1:

```sh
curl http://0.0.0.0:8081/m1
```
