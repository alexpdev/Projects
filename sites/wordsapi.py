import requests





def lookup_word(word):
    base = "https://wordsapiv1.p.rapidapi.com/words"
    headers = None
    url = base + "/" + word
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    print(response.json())
    return response

tests = [
    "application",
    "vampire",
    "compute",
    "theory",
    "organic",
]

for word in tests:
    lookup_word(word)
