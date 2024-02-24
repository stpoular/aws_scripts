import boto3
dynamo = boto3.client('dynamodb')

#####
# Put the entry for Danish into the LanguagesTable
#   "Language": "Danish"
#   "Code": "da"
#####
dynamo.put_item(
    TableName="LanguagesTable",
    Item={
         "Language" : {"S" : "Danish"},
         "Code" : {"S" : "da"},
          })

#####
# Retrieve the entry for Danish
#####
response = dynamo.get_item(
    TableName="LanguagesTable",
    Key={
        "Code": {"S": "da"}
        }
    )

print("")  # adds a blank line to format output
print(response['Item'])
print("")  # adds a blank line to format output
