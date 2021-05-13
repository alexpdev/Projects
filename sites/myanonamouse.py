import requests

URI = "https://t.myanonamouse.net"

def user_info(url=URI):
    rdict = {}
    request_url = url + "/jsonLoad.php"
    keys =  {"id":None,
        "notifs":None,
        "pretty":None,
        "snatch_summary":None}
    response = requests.get(request_url)
    rdict["json"] = response.json()
    rdict["url"] = response.url
    rdict["cookies"] = response.cookies
    rdict["headers"] = response.headers
    rdict["text"] = response.text
    return rdict

def print_response(response):
    print(response)



user_info()
