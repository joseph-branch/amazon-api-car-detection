import json
import requests
import boto3

CAR_TYPES = ["CAR", "TRUCK"]

keys = json.load(open("keys.json"))

key_id = keys["ID"]
access_key = keys["KEY"]
region = keys["REGION"]

client = boto3.client('rekognition',
                    aws_access_key_id = key_id,
                    aws_secret_access_key = access_key,
                    region_name = region)

photo = "TestFiles/drive-thru-line.png"

with open(photo, 'rb') as source_image:
    source_bytes = source_image.read()

response = client.detect_labels(Image = { 'Bytes': source_bytes })

response_labels = response["Labels"]

car_count = 0

for rl in response_labels:
    if(rl["Name"].upper() in CAR_TYPES):
        car_count += len(rl["Instances"])

url = f"http://localhost:3000/car-count/{car_count}"

car_response = requests.post(url)

print(f'Response Status Code: {car_response.status_code}')