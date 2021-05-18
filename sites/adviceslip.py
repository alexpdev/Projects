import requests
import json

base_url = "https://api.adviceslip.com/advice"

def get_advice(id=None):
    url = base_url
    if id:
        url += + "/" + str(id)
    response = requests.get(url)
    if response.status_code != 200:
        return ""
    slip = response.json()["slip"]
    print(slip)
    ID = slip["id"]
    advice = slip["advice"]
    return advice

def search_advice(query):
    url = base_url + "/search/" + query
    response = requests.get(url)
    if response.status_code != 200:
        return ""
    obj = response.json()
    count = obj["total_results"]
    slips = obj["slips"]
    return (count,slips)
