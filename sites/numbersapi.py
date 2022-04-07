import requests
import json

base_url = "http://numbersapi.com/"

def request_number(type_=None, number=0):
    url = base_url + str(number)
    if type_: url += "/" + type_
    response = requests.get(url)
    return response.text, response.json()
