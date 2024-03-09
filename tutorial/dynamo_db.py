'''
Code adapted from: https://www.coursera.org/learn/developing-applications-in-python-on-aws/
'''

import boto3


def add_entry(dynamo, language, code):
    dynamo.put_item(
        TableName="LanguagesTable",
        Item={
            "Language": {"S": language},
            "Code": {"S": code},
        })


def get_entry(dynamo, code):
    response = dynamo.get_item(
        TableName="LanguagesTable",
        Key={
            "Code": {"S": code}
        }
    )
    return response


def print_response(response):
    print("")  # adds a blank line to format output
    print(response['Item'])
    print("")  # adds a blank line to format output


def main():
    dynamo = boto3.client('dynamodb')

    '''
        Put the entry for Danish into the LanguagesTable
        "Language": "Danish"
        "Code": "da"
    '''
    add_entry(dynamo, "Danish", "da")

    '''
        Retrieve the entry for Danish
    '''
    response = get_entry(dynamo, "da")

    print_response(response)


if __name__ == '__main__':
    main()
