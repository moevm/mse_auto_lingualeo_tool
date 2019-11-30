import json

import requests


def get_json(response):
    decoded_response = response.content.decode('utf8')
    data = json.loads(decoded_response)
    return data


def dump_json(data):
    return json.dumps(data, indent=4, sort_keys=True)


base_url = 'https://api.lingualeo.com'
auth_url = 'https://lingualeo.com/ru/uauth/dispatch'
auth_data = {
    'email': 'pet.ai.4.uk@yandex.ru',
    'password': 'Wakeupman4981',
    'type': 'login',
}

get_words_url = base_url + '/GetWords'
gw_data = "{\"apiVersion\":\"1.0.0\",\"attrList\":{\"id\":\"id\",\"wordValue\":\"wd\",\"origin\":\"wo\",\"wordType\":\"wt\",\"translations\":\"trs\",\"wordSets\":\"ws\",\"created\":\"cd\",\"learningStatus\":\"ls\",\"progress\":\"pi\",\"transcription\":\"scr\",\"pronunciation\":\"pron\",\"relatedWords\":\"rw\",\"association\":\"as\",\"trainings\":\"trainings\",\"listWordSets\":\"listWordSets\",\"combinedTranslation\":\"trc\",\"picture\":\"pic\",\"speechPartId\":\"pid\",\"wordLemmaId\":\"lid\",\"wordLemmaValue\":\"lwd\"},\"category\":\"\",\"dateGroup\":\"start\",\"mode\":\"basic\",\"perPage\":30,\"status\":\"\",\"wordSetId\":16,\"offset\":null,\"search\":\"\",\"training\":null,\"ctx\":{\"config\":{\"isCheckData\":true,\"isLogging\":true}}}"
get_words_data = '''{
  "apiVersion": "1.0.1",
  "attrList": {
    "id": "id",
    "wordValue": "wd",
    "origin": "wo",
    "wordType": "wt",
    "translations": "trs",
    "wordSets": "ws",
    "created": "cd",
    "learningStatus": "ls",
    "progress": "pi",
    "transcription": "scr",
    "pronunciation": "pron",
    "relatedWords": "rw",
    "association": "as",
    "trainings": "trainings",
    "listWordSets": "listWordSets",
    "combinedTranslation": "trc",
    "picture": "pic",
    "speechPartId": "pid",
    "wordLemmaId": "lid",
    "wordLemmaValue": "lwd"
  },
  "category": "",
  "dateGroup": "start",
  "mode": "basic",
  "perPage": 999,
  "status": "",
  "wordSetId": 1,
  "offset": null,
  "search": "",
  "training": null,
  "ctx": {
    "config": {
      "isCheckData": true,
      "isLogging": true
    }
  }
}'''

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}


def get_wordset(wordset):
    session = requests.Session()
    response = session.post(auth_url, auth_data, headers=headers)
    response = session.options(get_words_url, headers=headers)
    response = session.post(get_words_url, get_words_data, headers=headers)

    words = get_json(response)['data']
    return words
