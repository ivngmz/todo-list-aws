#!/bin/bash

source todo-list-aws/bin/activate
set -x
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH: $PYTHONPATH"
export DYNAMODB_TABLE=todoUnitTestsTable
export ENDPOINT_OVERRIDE=`echo "http://"$(nslookup $(curl -s http://checkip.amazonaws.com) | grep name | awk '{print $4}' | sed 's/.$//')":8000"`
python test/unit/TestToDo.py
pip show coverage
coverage run --include=src/todoList.py test/unit/TestToDo.py
coverage report -m
coverage report
coverage xml