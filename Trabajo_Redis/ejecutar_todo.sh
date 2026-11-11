#!/bin/bash

# Se detendrá la ejecución si ocurre algún error
set -e

echo "------------------------------------------------------------------------"
echo ""
echo "   AUTOMATIZACIÓN DE INFRAESTRUCTURA Y DATOS (DOCKER)  "

# 1. Se comprueban contenedores antiguos si existen y levanta de nuevo
echo -e "\n1. Reiniciando contenedores Docker..."

# Apaga cualquier contenedor de cualquier carpeta que esté usando puertos
docker stop $(docker ps -q) 2>/dev/null || true

# Limpia el proyecto actual y levanta los contenedores de nuevo
docker compose down -v
docker compose up -d --force-recreate

# 2. Se esperará a que los motores de Base de Datos estén totalmente listos
# (Docker levanta el contenedor en 1 seg, pero MySQL/Postgres tardan unos segundos en arrancar el servicio)
echo -e "\n2. Esperando 30 segundos a que las bases de datos inicien el servicio SQL..."
sleep 30

# 3. Se activará el entorno virtual si existe
if [ -d "venv" ]; then
    echo -e "\n3. Activando entorno virtual..."
    source venv/bin/activate
fi

# 4. Se ejecutará la creación de tablas y poblado de datos
echo -e "\n4. Ejecutando la creación de tablas..."
python3 crea_tablas.py

echo -e "\n5. Poblando las bases de datos con datos de prueba..."
python3 rellena_bdd.py

echo -e "------------------------------------------------------------------------"
echo "PROCESO FINALIZADO: VÍA LIBRE"