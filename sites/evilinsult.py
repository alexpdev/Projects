import requests

base_url = "http://evilinsult.com/api"

def get_insult(lang="en",type_="json"):
    url = base_url + "/generate_insult.php"
    params = {"type":type_,"lang":lang}
    response = requests.get(url,params=params)
    return response.text
