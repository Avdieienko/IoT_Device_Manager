import boto3
import json
import boto3.session
from botocore.exceptions import ClientError, NoCredentialsError

from urllib import parse


def configure_aws_user():
  """ Configures AWS account based on config.json file, located in the same folder.

  Returns:
      AWS-Session: Session for a camera user
  """
  config = {}

  try:
    with open("account_config.json") as config_json:
        config = json.load(config_json)
  except Exception as e:
    print(f"Error loading config: {e}")
    return None

  session = boto3.Session(
    aws_access_key_id=config["access_key_id"],
    aws_secret_access_key=config["secret_access_key"],
    region_name=config["region"],
    aws_session_token=None ,
  )

  return session

def configure_IoT_device(session):
  """ Configures AWS account based on device_config.json file, located in the same folder.

  Returns:
      AWS-Session: Session for a camera user
  """
  config = {}

  tags = {}

  try:
    with open("device_config.json") as config_json:
      config = json.load(config_json)
  except Exception as e:
    print(f"Error loading config: {e}")
    return None

  tags["deviceName"] = config["deviceName"]
  tags["cameraType"] = config["cameraType"]
  tags["deviceType"] = config["deviceType"]

  if "deviceID" in config:
    tags["deviceID"] = config["deviceID"]
  else:
    try:
      credentials = assume_role(session, "register_device", None, "RegisterDeviceRole")

      dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name=session.region_name
      )


      table = dynamodb.Table('registered_devices')
      items = table.scan()["Items"]
      print(f"Items: {items}")

      # Retrieve the item count from the table description
      item_count = len(items)
      print(f"Item count: {item_count}")

      if item_count >= 10:
        print("Table is full")
        raise Exception("Table is full")

      deviceID = f"1034{item_count + 1}298"
      tags["deviceID"] = deviceID

      table.put_item(
        Item={
          "deviceID":  deviceID,
          "cameraType": config["cameraType"],
          "deviceName": config["deviceName"],
          "deviceType":  config["deviceType"]
        }
      )

      # write the deviceID to the config file
      with open("device_config.json", "w") as config_json:
        json.dump(tags, config_json)
    except Exception as e:
      print(f"Error regsitering device: {e}")
      return None


  return tags

def assume_role(console, session_name, role_tags, role_name):
  if role_tags:
    role_tags = [{'Key': key, 'Value': value} for key, value in role_tags.items()]
  else:
    role_tags = []

  sts_client = console.client("sts")
  id = sts_client.get_caller_identity()["Account"]
  try:
    response = sts_client.assume_role(
      RoleArn=f"arn:aws:iam::{id}:role/{role_name}",
      RoleSessionName=session_name,
      Tags = role_tags,
      DurationSeconds=1200,
    )
  except ClientError as e:
    print(f"Error assuming role: {e}")
    return None

  return response['Credentials']

def upload_to_s3_with_temporary_credentials(file_name, bucket, object_name, temp_creds, tags):
  """Upload a file to an S3 bucket with tags using temporary credentials."""
  s3_client = boto3.client(
    's3',
    aws_access_key_id=temp_creds['AccessKeyId'],
    aws_secret_access_key=temp_creds['SecretAccessKey'],
    aws_session_token=temp_creds['SessionToken']
  )

  # Convert tags dictionary to the required format

  try:
    # Upload the file with tags
    s3_client.upload_file(
        file_name,
        bucket,
        object_name,
        ExtraArgs={"Tagging": parse.urlencode(tags)}
    )
    print(f"File {file_name} uploaded to {bucket}/{object_name}")
    return True
  except FileNotFoundError:
    print("The file was not found")
    return False
  except NoCredentialsError:
    print("Credentials not available")
    return False
  except ClientError as e:
    print(f"Error uploading file: {e}")
    return False
