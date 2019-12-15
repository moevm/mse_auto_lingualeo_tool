import requests
import json


# Класс для работы с сервисом Lingualeo
class lingualeo_service:
    def __init__(self, email, password):
        self.session = requests.Session()
        self.email = email
        self.password = password
        

    # Авторизация в Lingauleo, необходимое для дальнейшей работы
    def auth(self):
        url = 'https://lingualeo.com/ru/uauth/dispatch'
        params = {'email': self.email, 'password': self.password, 'type': 'login'}
        response = self.session.post(url, data=params)
        return json.loads(response.text)


    # Функция добавления одного слова в набор слов Lingualeo
    def add_word(self, word, translate, context):
        url = 'https://api.lingualeo.com/AddWord'
        params = {'word': word, 'tword': translate, 'context': context, 'port': '1001'}
        response = self.session.post(url, data=params)
        return json.loads(response.text)


    # Функция создания набора слов с данным именем
    def create_words_set(self, name):
        url = 'https://api.lingualeo.com/SetWordSets'
        params = {
          "apiVersion": "1.0.0",
          "op": "createWordSet",
          "data": [
            {
              "action": "add",
              "valueList": {
                "name": "Название набора",
                "picture": None
              }
            }
          ],
          "ctx": {
            "config": {
              "isCheckData": True,
              "isLogging": True
            }
          }
        }
        print(json.dumps(params))
        response = self.session.post(url, data=json.dumps(params))
        return json.loads(response.text)

