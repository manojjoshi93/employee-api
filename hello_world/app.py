import boto3
import json
from flask_lambda import FlaskLambda
from flask import request
from botocore.exceptions import ClientError

app = FlaskLambda(__name__)
ddb = boto3.resource("dynamodb")
table = ddb.Table('employee')

# @app.route('/')
# def index():
#     return json_response({'message': 'Hello, welcome to employee website'})

@app.route('/employee', methods=["GET", 'POST'])
def put_or_list_employee():
    try:
        if request.method == 'GET':
            employees = table.scan()['Items']
            return json_response(employees)
        else:
            table.put_item(Item=request.form.to_dict())
            return json_response({'message': 'employee entry updated'})
    except ClientError as err:
        print(err)

@app.route('/employee/<id>', methods=["GET", "PATCH", "DELETE"])
def get_patch_delete(id):
    if request.method == 'GET':
        emp_detail = table.get_item(Key={'id':id })['Item']
        return json_response(emp_detail)
    elif request.method == 'PATCH':
        attribute_updates = {key:{'Value':value, 'Action': 'PUT'}
                            for key, value in request.form.items()}
        table.update_item(Key={'id': id}, AttributeUpdates=attribute_updates)
        return json_response({"message": "employee entry updated"})
    else:
        table.delete_item(Key={'id': id})
        return json_response({'message': 'employee entry deleted'})

def json_response(data, response_code = 200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}

# Use below lambda_handler to - Pass environment variables when invoking a Lambda function locally
def lambda_handler(event, context):
    try:
        employees = table.scan()['Items']
        return json_response(employees)
    except ClientError as err:
        print(err)

# We want to locally test our Lambda function while having it interact with our DynamoDB table in the cloud. 
# To do this, we create our environment variables file and save it in our project's root directory as locals.json. 
# The value provided here for SAMPLE_TABLE references our DynamoDB table in the cloud.

# Tip: You can run postapi.py to insert the values in DDB table first and then invoke lambda locally
# Next, we run below command; sam local invoke and pass in our environment variables with the --env-vars option.
# $ sam local invoke getAllItemsFunction --env-vars locals.json

# update handler in template.json to Handler: app.lambda_handler

    # return {
    #     "statusCode": 200,
    #     "body": json.dumps({
    #         "message": "hello world",
    #         # "location": ip.text.replace("\n", "")
    #     }),
    # }
