#!/bin/bash

source todo-list-aws/bin/activate
set -x
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH: $PYTHONPATH"
docker start eed9128e1f0d
export DYNAMODB_TABLE=todoUnitTestsTable
echo "https://"$Stage"-TodosDynamoDbTable"
#export ENDPOINT_OVERRIDE="${Stage}-TodosDynamoDbTable"
#"http://127.0.0.1:8000"
nc -vz 127.0.0.1 8000
echo "Iniciando dynamodb en local ..."
aws dynamodb create-table --table-name dynamodb --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --endpoint-url http://localhost:8000
echo "Mostrando tablas ..."
aws dynamodb list-tables --endpoint-url http://127.0.0.1:8000
python test/unit/TestToDo.py
pip show coverage
coverage run --include=src/todoList.py test/unit/TestToDo.py
coverage report -m
coverage report
coverage xml
docker stop eed9128e1f0d