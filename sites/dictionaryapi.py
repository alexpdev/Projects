import requests

def defenition(word,lang="en_US"):
    site = "https://api.dictionaryapi.dev/api/v2/entries"
    url = site + "/" + lang + "/" + word
    resp = requests.get(url)
    return resp.json()




language_codes = {
    "English" : "en_US",
    "Hindi" : "hi",
    "Spanish" : "es",
    "French" : "fr",
    "Japanese" : "ja",
    "Russian" : "ru",
    "English(UK)" : "en_GB",
    "German" : "de",
    "Italian" : "it",
    "Korean" : "ko",
    "Arabic" : "ar",
    "Turkish" : "tr"
}
