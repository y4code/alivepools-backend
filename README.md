# alivepools-backend

# Install
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

# Freeze dependencies
```shell
pip3 freeze > requirements.txt
```

# Run
run local server
```shell
flask --app alivepools-backend run
```

run on production server
```shell
flask --app alivepools-backend run --host=0.0.0.0
```

run on production server with nohup
```shell
nohup flask --app alivepools-backend run --host=0.0.0.0 &
```

# About Caddyfile
Just run command below to start caddy server in background
```shell
caddy start
```