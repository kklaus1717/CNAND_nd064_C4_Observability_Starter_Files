import time
import random
import requests


def make_request(uri):
    try:
        response = requests.get(f"http://localhost:8081/{uri}")
        if response.status_code == 200:
            print("Response:", response.text)
        else:
            print("Failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)

while True:
    make_request("")
    make_request("api")
    make_request("slow")
    make_request("error400")    
    make_request("error500")
    time.sleep(random.uniform(0, 1))

