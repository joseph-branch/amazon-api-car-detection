import json
import requests
import boto3

class CarDetection():
    CAR_TYPES = ["CAR", "TRUCK"]

    def __init__(self, photo):
        try:
            self.photo = photo
            self.car_count = 0

            self.url = f"http://localhost:3000/car-count"
        except:
            print("Init failed...")


    def getCredentials(self):
        try:
            keys = json.load(open("keys.json"))

            self.key_id = keys["ID"]
            self.access_key = keys["KEY"]
            self.region = keys["REGION"]
        except:
            print("Failed to get credentials...")

    def getImageBytes(self):
        try:
            with open(self.photo, 'rb') as source_image:
                self.source_bytes = source_image.read()
        except:
            print("Failed to get image bytes")

    def initAmazonApi(self):
        try:
            self.amazon_client = boto3.client('rekognition',
                        aws_access_key_id = self.key_id,
                        aws_secret_access_key = self.access_key,
                        region_name = self.region)
        except:
            print("Failed to initialize amazon client...")

    def getAmazonApiCarCount(self):
        try:
            response = self.amazon_client.detect_labels(Image = { 'Bytes': self.source_bytes })
            response_labels = response["Labels"]

            car_count = 0

            for rl in response_labels:
                if(rl["Name"].upper() in self.CAR_TYPES):
                    car_count += len(rl["Instances"])
            
            return car_count
        except:
            print("Failed to get car count from amazon api...")

    def getServerCarCount(self):
        try:
            self.response = requests.get(self.url)
            self.displayResponse()
        except:
            print("Failed to get response from server")

    def postServerCarCount(self):
        try:
            car_count = self.getAmazonApiCarCount()
            self.response = requests.post(f'{self.url}/{car_count}')
            self.displayResponse()
        except:
            print("Failed to post to server")

    def displayResponse(self):
        try:
            if (self.response.status_code == 200):
                if(bool(self.response.content)):
                    print(f'Current car count: {self.response.json()["CAR_COUNT"]}')
        except:
            print(f'Response Status Code: {self.response.status_code}')
            print("Failed to get response status code")

    def run(self):
        self.getCredentials()
        self.getImageBytes()
        self.initAmazonApi()

if __name__ == "__main__":
    Car_Detection_Obj = CarDetection(f'TestFiles/drive-thru-line.png')
    Car_Detection_Obj.run()

    Car_Detection_Obj.getServerCarCount()
    Car_Detection_Obj.postServerCarCount()
    Car_Detection_Obj.getServerCarCount()