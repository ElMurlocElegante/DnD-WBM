#!/bin/bash

function install_dependencies() {
    if ! pipenv --version &> /dev/null # Verifica si pipenv está instalado
    then
        echo "pipenv no está instalado. Instalando pipenv..."
        pip install pipenv
    fi

    echo "Instalando dependencias del proyecto..." # Instala las dependencias del proyecto
    pipenv install
}

function start_application() {
    source $(pipenv --venv)/bin/activate # Activa el entorno virtual
    export FLASK_DEBUG=1 # Activo modo debug de flask
    flask run # Activo server
}

echo "Seleccione una opción:"
echo "1. Instalar dependencias e iniciar la aplicación"
echo "2. Solo iniciar la aplicación"
read -p "Ingrese su elección [1 o 2]: " choice

case $choice in
    1)
        install_dependencies
        start_application
        ;;
    2)
        start_application
        ;;
    *)
        echo "Opción no válida. Por favor, ejecute el script nuevamente y seleccione una opción válida."
        ;;
esac
