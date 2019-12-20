import json
import requests


# Класс для работы с сервисом Lingualeo
class LingualeoService:
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


    # Функция добавления одного слова в Lingualeo
    def add_word(self, word, translate, context):
        url = 'https://api.lingualeo.com/AddWord'
        params = {'word': word, 'tword': translate, 'context': context, 'port': '1001'}
        response = self.session.post(url, data=params)
        return json.loads(response.text)


    # Функция добавления набора слов в Lingualeo
    def add_words_set(self, words_set):
        count = 1
        for elem in words_set:
            self.add_word(elem["word"], elem["translation"], '')
            print('\r{0}/{1}'.format(count, len(words_set)), end='')
            count += 1
        print()


    # Функция создания набора слов с данным именем
    def create_words_set(self, name):
        url = 'https://api.lingualeo.com/SetWordSets'
        options_headers = {
            'Host': 'api.lingualeo.com',
            'Access-Control-Request-Method': 'POST',
            'Origin': 'https://lingualeo.com',
            'Access-Control-Request-Headers': 'content-type',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://lingualeo.com/ru/dictionary/sets/my',
        }
        post_headers = {
            'Host': 'api.lingualeo.com',
            'Accept': 'application/json',
            'Origin': 'https://lingualeo.com',
            'Content-type': 'application/json',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://lingualeo.com/ru/dictionary/sets/my',
        }
        params = '{"apiVersion":"1.0.0","op":"createWordSet","data":[{"action":"add","valueList":{"name":"%s","picture":null}}],"ctx":{"config":{"isCheckData":true,"isLogging":true}}}' % name
        options_response = self.session.options(url, headers=options_headers)
        post_response = self.session.post(url, data=params.encode('utf-8'), headers=post_headers)
        return json.loads(post_response.text)
