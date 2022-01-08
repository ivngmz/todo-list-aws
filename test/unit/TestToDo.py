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

    def test_describe_missing_table_boto3(self):
        print ('Start: test_describe_missing_table_boto3')
        with pytest.raises(ClientError) as ex:
            self.dynamodb.describe_table(TableName="messages")
        ex.value.response["Error"]["Code"].should.equal("ResourceNotFoundException")
        print ('End: test_describe_missing_table_boto3')
    
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

    def test_table_exists_error(self):
        print ('---------------------')
        print ('Start: test_table_exists_error')
        from src.todoList import get_item
        from src.todoList import create_todo_table
        print("Comprobando la existencia de la tabla antes borrado...")
        print("Existe: " + str(self.assertTrue(self.table.name)))
        self.dynamodb = None
        print("Comprobando la existencia de la tabla tras borrado...")
        print("Existe: " + str(self.assertTrue(self.table.name)))  # check if we got a result
        print ('End: test_table_exists_error')

    def test_get_table_error_KeyError(self):
        print ('---------------------')
        print ('Start: test_get_table_error_KeyError')
        from src.todoList import get_item
        try:
            response = get_item("")
            print(response)
        except KeyError:
            print("Se ha generado la excepcion:KeyError")
        print ('End: test_get_table_error_KeyError')        

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
            with pytest.raises(botocore.exceptions.ClientError(MSG_TEMPLATE,put_item("", self.dynamodb))) as exc_info:
                print("Imprimo Error")
        except AttributeError as e:
            print("Imprimo Error")

    def test_get_todo(self):
        print ('---------------------')
        print ('Start: test_get_todo')
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
        from src.todoList import get_item
        try:
            get_item("Esto no existe",self.dynamodb)
        except botocore.exceptions.ClientError as error:
            print("Se ha levantado la excepcion:ClientError")
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
            with pytest.raises(botocore.exceptions.ClientError(MSG_TEMPLATE,update_item("@@@@","","",self.dynamodb))) as exc_info:
                print("Imprimo Error: " + str(exc_info))
        except AttributeError as e:
            responseUpdateError = update_item("@@@@","","",self.dynamodb)
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
        print ('Response PutItem' + str(responsePut))
        idItem = json.loads(responsePut['body'])['id']
        print ('Id item:' + idItem)
        delete_item(idItem, self.dynamodb)
        print ('Item deleted succesfully')
        self.assertTrue(len(get_items(self.dynamodb)) == 0)
        print ('End: test_delete_todo')

    def test_delete_todo_error(self):
        print ('---------------------')
        print ('Start: test_delete_todo_error')
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
            with pytest.raises(botocore.exceptions.ClientError(MSG_TEMPLATE,delete_item("@@@@",self.dynamodb))) as exc_info:
                print("Imprimo Error: " + str(exc_info))
        except AttributeError as exc_info:
            responseDeleteError = delete_item("@@@@",self.dynamodb)
            print("Imprimo Error: " + str(exc_info))
        print ('End: test_delete_todo_error')
    

if __name__ == '__main__':
    unittest.main()
