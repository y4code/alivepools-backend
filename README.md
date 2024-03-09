# alivepools-backend

[![Deploy alivepools-backend to Server](https://github.com/y4code/alivepools-backend/actions/workflows/deploy.yml/badge.svg)](https://github.com/y4code/alivepools-backend/actions/workflows/deploy.yml)

## How to Run

Install dependencies

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

**Local**
```shell
flask --app alivepools-backend run
```

**Production**
```shell
flask --app alivepools-backend run --host=0.0.0.0
```

**Production with `systemd` (Recommend)**

Put [alivepools-backend.service](alivepools-backend.service) in `/etc/systemd/system/`, run `daemon-reload`, `enable` and `start` command before command below

```shell
sudo systemctl restart alivepools-backend.service
```

## Cheatsheet

**Freeze dependencies**

```shell
pip3 freeze > requirements.txt
```

**Caddyfile**

check [Caddyfile](Caddyfile) for more details

```shell
caddy start
```
