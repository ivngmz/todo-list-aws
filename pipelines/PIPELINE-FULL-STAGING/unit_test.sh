#!/bin/bash

source todo-list-aws/bin/activate
set -x
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH: $PYTHONPATH"
export DYNAMODB_TABLE=todoUnitTestsTable
echo "https://"$Stage"-TodosDynamoDbTable"
#export ENDPOINT_OVERRIDE="${Stage}-TodosDynamoDbTable"
export ENDPOINT_OVERRIDE="http://127.0.0.1:8000"
nc -vz 127.0.0.1 8000
if [ $? != 0 ]; then
        echo "El contenedor docker de dynamodb no está levantado"
        exit 1
    fi
echo "Mostrando tablas ..."
aws dynamodb list-tables --endpoint-url http://127.0.0.1:8000 --endpoint-url http://localhost:8000 --region us-east-1
python test/unit/TestToDo.py
pip show coverage
coverage run --include=src/todoList.py test/unit/TestToDo.py
coverage report -m
coverage report
coverage xml