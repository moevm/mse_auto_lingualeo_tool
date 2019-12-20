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


    # Функция получения списка наборов слов TODO
    def get_word_sets(self):
        url = 'https://api.lingualeo.com/GetWordSets'
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
        params = '{"apiVersion":"1.0.0","op":"loadSets:[{\"req\":\"myAll\",\"opts\":{\"category\":\"all\",\"page\":1,\"perPage\":20},\"attrs\":[\"type\",\"id\",\"name\",\"countWords\",\"countWordsLearned\",\"picture\",\"category\",\"status\",\"source\",\"level\"]}]","request":[{"subOp":"myAll","type":"user","perPage":999,"sortBy":"created","attrList":{"type":"type","id":"id","name":"name","countWords":"cw","countWordsLearned":"cl","wordSetId":"wordSetId","picture":"pic","category":"cat","status":"st","source":"src"}}],"ctx":{"config":{"isCheckData":true,"isLogging":true}}}'
        options_response = self.session.options(url, headers=options_headers)
        post_response = self.session.post(url, data=params.encode('utf-8'), headers=post_headers)
        return json.loads(post_response.text)


    # Функция получения слов из конкретного набора слов
    def get_words(self, word_set_id):
        url = 'https://api.lingualeo.com/GetWords'
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
        params = '{"apiVersion":"1.0.1","attrList":{"id":"id","wordValue":"wd","origin":"wo","wordType":"wt","translations":"trs","wordSets":"ws","created":"cd","learningStatus":"ls","progress":"pi","transcription":"scr","pronunciation":"pron","relatedWords":"rw","association":"as","trainings":"trainings","listWordSets":"listWordSets","combinedTranslation":"trc","picture":"pic","speechPartId":"pid","wordLemmaId":"lid","wordLemmaValue":"lwd"},"category":"","dateGroup":"start","mode":"basic","perPage":30,"status":"","wordSetId":%s,"offset":null,"search":"","training":null,"ctx":{"config":{"isCheckData":true,"isLogging":true}}}' % word_set_id
        options_response = self.session.options(url, headers=options_headers)
        post_response = self.session.post(url, data=params.encode('utf-8'), headers=post_headers)
        return json.loads(post_response.text)


    # Функция получения перевода слова TODO
    def get_translate(self, word):
        url = 'https://api.lingualeo.com/gettranslates'
        post_headers = {
            'Host': 'api.lingualeo.com',
            'Connection': 'close',
            'Content-Length': '61',
            'Sec-Fetch-Mode': 'cors',
            'X-Accept-Language': 'ru',
            'LinguaLeo-Version': '2.0.3.4',
            'User-Agent': '{...}',
            'DNT': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': '{...}'
        }
        params = '{"word":%s,"include_media":"1","add_word_forms":"1","port":"1001"}' % word
        post_response = self.session.post(url, data=params.encode('utf-8'), headers=post_headers)
        return json.loads(post_response.text)


    # Функция добавления одного слова в Lingualeo
    def add_word(self, word, translate, context):
        url = 'https://api.lingualeo.com/AddWord'
        params = {'word': word, 'tword': translate, 'context': context, 'port': '1001'}
        response = self.session.post(url, data=params)
        return json.loads(response.text)


    # Функция добавления набора слов в Lingualeo
    def add_words_set(self, word_set):
        count = 1
        print("Добавление слов в Lingualeo...")
        for elem in word_set:
            self.add_word(elem["word"], elem["translation"], '')
            print('\r{0}/{1}'.format(count, len(word_set)), end='')
            count += 1
        print()
        print("Слова в Lingualeo добавлены!")


    # Функция создания набора слов с данным именем
    def create_word_set(self, name):
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
