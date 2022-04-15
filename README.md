# Streamlabs test app

Small python app that takes care of the authorization, authentication, token gathering and token store for the RTL
project

## How to run

To run this you need to create a virtual environment and install the packages in requirements.txt
```shell
python -m venv lab
source lab/bin/activate
pip install -r requirements.txt
```

To get out of the venv, enter the following command
```shell
deactivate
```

### API

To run the program you need to be sure that the venv is active and then run
```shell
uvicorn api.app:app --reload
```

### Socket

To run the standalone socket part
```shell
python -m standalone.sockets
```