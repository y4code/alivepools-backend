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
```shell
flask --app alivepools-backend run
or
flask --app alivepools-backend run --host=0.0.0.0 --port=80
```