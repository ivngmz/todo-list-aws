# from pprint import pprint
import warnings
import unittest
import pytest
import boto3
import botocore
from moto import mock_dynamodb2, mock_dynamodb2_deprecated
from botocore.exceptions import ClientError
import sys
import os
import json
from botocore.utils import get_service_module_name

@mock_dynamodb2_deprecated
@mock_dynamodb2
class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        print ('---------------------')
        print ('Start: setUp')
        warnings.filterwarnings(
            "ignore",
            category=ResourceWarning,
            message="unclosed.*<socket.socket.*>")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="callable is None.*")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="Using or importing.*")
        """Create the mock database and table"""
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.is_local = 'true'
        self.uuid = "123e4567-e89b-12d3-a456-426614174000"
        self.text = "Aprender DevOps y Cloud en la UNIR"

        from src.todoList import create_todo_table
        self.table = create_todo_table(self.dynamodb)
        #self.table_local = create_todo_table()
        print ('End: setUp')

    def tearDown(self):
        print ('---------------------')
        print ('Start: tearDown')
        """Delete mock database and table after test is run"""
        self.table.delete()
        print ('Table deleted succesfully')
        #self.table_local.delete()
        self.dynamodb = None
        print ('End: tearDown')

    def test_table_exists(self):
        print ('---------------------')
        print ('Start: test_table_exists')
        self.assertTrue(self.table)  # check if we got a result
        #self.assertTrue(self.table_local)  # check if we got a result
        
        print('Table name:' + self.table.name)
        tableName = os.environ['DYNAMODB_TABLE'];
        # check if the table name is 'ToDo'
        self.assertIn(tableName, self.table.name)
        #self.assertIn('todoTable', self.table_local.name)
        print ('End: test_table_exists')

    def test_put_todo(self):
        print ('---------------------')
        print ('Start: test_put_todo')
        # Testing file functions
        from src.todoList import put_item
        # Table local
        response = put_item(self.text, self.dynamodb)
        print ('Response put_item:' + str(response))
        self.assertEqual(200, response['statusCode'])
        #Table mock
        print ('End: test_put_todo')

    def test_put_todo_error(self):
        print ('---------------------')
        print ('Start: test_put_todo_error')
        conn = boto3.client('dynamodb', region_name='us-east-1')
        # Testing file functions
        from src.todoList import put_item
        from src.todoList import get_item
        # Table mock
        self.assertRaises(Exception, put_item("", self.dynamodb))
        self.assertRaises(Exception, get_item("", self.dynamodb))

        MSG_TEMPLATE = (
        'An error occurred (400) when calling the put_item '
        'operation1:lse')
        try:
            with pytest.raises(self.dynamodb.ClientError(MSG_TEMPLATE,put_item("", self.dynamodb))) as exc_info:
                error_code = exc_info.response['Error']['Code']
                print(error_code)
        except AttributeError as e:
            print("Imprimo Error")

    def test_get_todo(self):
        print ('---------------------')
        print ('Start: test_get_todo')
        conn = boto3.client('dynamodb', region_name='us-east-1')
        from src.todoList import get_item
        from src.todoList import put_item

        # Testing file functions
        # Table mock
        responsePut = put_item(self.text, self.dynamodb)
        print ('Response put_item:' + str(responsePut))
        idItem = json.loads(responsePut['body'])['id']
        print ('Id item:' + idItem)
        self.assertEqual(200, responsePut['statusCode'])
        responseGet = get_item(
                idItem,
                self.dynamodb)
        print ('Response Get:' + str(responseGet))
        self.assertEqual(
            self.text,
            responseGet['text'])
        print ('End: test_get_todo')
        
    def test_get_todo_error_ClientError(self):
        print ('---------------------')
        print ('Start: test_get_todo_error_ClientError')
        conn = boto3.client('dynamodb', region_name='us-east-1')
        from src.todoList import get_item
        try:
            get_item("Esto no existe",self.dynamodb)
        except self.dynamodb.ClientError as exc_info:
            error_code = exc_info.response['Error']['Code']
            print(error_code)
        print ('End: test_get_todo_error_ClientError')
    
    def test_list_todo(self):
        print ('---------------------')
        print ('Start: test_list_todo')
        from src.todoList import put_item
        from src.todoList import get_items

        # Testing file functions
        # Table mock
        put_item(self.text, self.dynamodb)
        result = get_items(self.dynamodb)
        print ('Response GetItems' + str(result))
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0]['text'] == self.text)
        print ('End: test_list_todo')


    def test_update_todo(self):
        print ('---------------------')
        print ('Start: test_update_todo')
        from src.todoList import put_item
        from src.todoList import update_item
        from src.todoList import get_item
        updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"
        # Testing file functions
        # Table mock
        responsePut = put_item(self.text, self.dynamodb)
        print ('Response PutItem' + str(responsePut))
        idItem = json.loads(responsePut['body'])['id']
        print ('Id item:' + idItem)
        result = update_item(idItem, updated_text,
                            "false",
                            self.dynamodb)
        print ('Result Update Item:' + str(result))
        self.assertEqual(result['text'], updated_text)
        print ('End: test_update_todo')


    def test_update_todo_error(self):
        print ('---------------------')
        print ('Start: test_update_todo_error')
        conn = boto3.client('dynamodb', region_name='us-east-1')
        from src.todoList import put_item
        from src.todoList import update_item
        updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"
        # Testing file functions
        # Table mock
        responsePut = put_item(self.text, self.dynamodb)
        print ('Response PutItem' + str(responsePut))
        self.assertRaises(
            Exception,
            update_item(
                updated_text,
                "",
                "false",
                self.dynamodb))
        self.assertRaises(
            TypeError,
            update_item(
                "",
                self.uuid,
                "false",
                self.dynamodb))
        self.assertRaises(
            Exception,
            update_item(
                updated_text,
                self.uuid,
                "",
                self.dynamodb))
        
        MSG_TEMPLATE = (
        'An error occurred (400) when calling the put_item '
        'operation1:lse')
        
        try:
            with pytest.raises(self.dynamodb.ClientError(MSG_TEMPLATE,update_item("","","",""))) as exc_info:
                error_code = exc_info.response['Error']['Code']
                print(error_code)
        except AttributeError as e:
            responseUpdateError = update_item("@@@@","","false",self.dynamodb)
            print("Imprimo Error: " + str(responseUpdateError))
        
        print ('End: test_update_todo_error')

    def test_delete_todo(self):
        print ('---------------------')
        print ('Start: test_delete_todo')
        from src.todoList import delete_item
        from src.todoList import put_item
        from src.todoList import get_items
        # Testing file functions
        # Table mock
        responsePut = put_item(self.text, self.dynamodb)
        totalItems = len(get_items(self.dynamodb))
        print ('Total Items tras put: ' + str(totalItems))
        print ('Response PutItem' + str(responsePut))
        idItem = json.loads(responsePut['body'])['id']
        print ('Id item: ' + idItem)
        responseDel = print(delete_item(idItem, self.dynamodb))
        totalItems = len(get_items(self.dynamodb))
        if (totalItems == 0):
            print ('Item ' + idItem + ' deleted succesfully')
        print ('Total Items tras delete: ' + str(totalItems))
        self.assertTrue(len(get_items(self.dynamodb)) == 0)
        print ('End: test_delete_todo')

    def test_delete_todo_error(self):
        print ('---------------------')
        print ('Start: test_delete_todo_error')
        conn = boto3.client('dynamodb', region_name='us-east-1')
        from src.todoList import delete_item
        from src.todoList import put_item
        # Testing file functions
        responsePut = put_item(self.text, self.dynamodb)
        idItem = json.loads(responsePut['body'])['id']
        print ('Intento Borrar dos veces el Id item:' + idItem)
        print(delete_item(idItem, self.dynamodb))
        print(delete_item(idItem, self.dynamodb))
        
        self.assertRaises(TypeError, delete_item("", self.dynamodb))
        
        MSG_TEMPLATE = (
        'An error occurred (400) when calling the put_item '
        'operation1:lse')
        
        self.assertRaises(
            Exception,
            delete_item(
                "@@@@",
                self.dynamodb))
        self.assertRaises(
            TypeError,
            delete_item(
                "@@@@",
                self.dynamodb))
        self.assertRaises(
            Exception,
            delete_item(
                "@@@@",
                self.dynamodb))
        try:
            with pytest.raises(self.dynamodb.ClientError(MSG_TEMPLATE,delete_item("@@@@",self.dynamodb))) as exc_info:
                error_code = exc_info.response['Error']['Code']
                print(error_code)
        except AttributeError as exc_info:
            responseDeleteError = delete_item("@@@@",self.dynamodb)
            print("Imprimo Error: " + str(exc_info))
        print ('End: test_delete_todo_error')
    

if __name__ == '__main__':
    unittest.main()
