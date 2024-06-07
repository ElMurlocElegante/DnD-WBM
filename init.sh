#!/bin/bash

source $(pipenv --venv)/bin/activate  # Activa el entorno virtual
export FLASK_DEBUG=1 # Activo modo debug de flask
flask run # Activo server
