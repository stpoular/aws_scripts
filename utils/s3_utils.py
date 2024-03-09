import boto3


def dir_s3_bucket(source_bucket):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=source_bucket)
    filenames = [obj["Key"] for obj in response["Contents"]]
    count = len(filenames)

    return filenames, count


def read_s3_file(source_bucket, filename):
    # get the contents of a file in the s3 bucket
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=source_bucket, Key=filename)
    file_data = response['Body'].read()
    return file_data


def write_s3_file(filename, destination_bucket, destination_key):
    with open(filename, 'rb') as data:
        # copy a file to a randomly named object in the destination bucket
        s3 = boto3.client("s3")
        s3.put_object(
            Bucket=destination_bucket,
            Key=destination_key,
            Body=data,
            ContentType='image/jpg'
        )

    print(f"Saved file to s3 bucket: {destination_bucket}, key: {destination_key}\n\n")


def create_presigned_url(bucket, key, expiration_minutes):
    # build a presigned URL for the s3 bucket
    s3 = boto3.client("s3")
    presigned_url = s3.generate_presigned_url("get_object",
                                              Params={
                                                  "Bucket": bucket,
                                                  "Key": key},
                                              ExpiresIn= expiration_minutes * 60)
    return presigned_url
