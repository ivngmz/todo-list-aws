#!/bin/bash

source todo-list-aws/bin/activate
set -x
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH: $PYTHONPATH"
export DYNAMODB_TABLE=todoUnitTestsTable
export ENDPOINT_OVERRIDE="http://127.0.0.1:8000"
docker start dynamodb
if [ $? != 0 ]; then    
        ## Crear red de docker
        docker network create sam

        ## Levantar el contenedor de dynamodb en la red de sam con el nombre de dynamodb
        docker run -p 8000:8000 --network sam --name dynamodb -d amazon/dynamodb-local
    fi
nc -vz 127.0.0.1 8000
if [ $? != 0 ]; then
        echo "El contenedor docker de dynamodb no está levantado, debe haber un problema"
        exit 1
    fi
aws dynamodb create-table --table-name local-TodosDynamoDbTable --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --endpoint-url http://localhost:8000 --region us-east-1
echo "Mostrando tablas ..."
aws dynamodb list-tables --endpoint-url http://127.0.0.1:8000 --region us-east-1
python -d test/unit/TestToDo.py
pip show coverage
coverage run --include=src/todoList.py test/unit/TestToDo.py
coverage report -m
coverage report
coverage xml