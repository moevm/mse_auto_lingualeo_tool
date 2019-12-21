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
        params = {
          "apiVersion": "1.0.0",
          "op": "loadSets: \n[\n  {\n    \"req\": \"myAll\",\n    \"opts\": {\n      \"category\": \"all\",\n      \"page\": 1,\n      \"perPage\": 20\n    },\n    \"attrs\": [\n      \"type\",\n      \"id\",\n      \"name\",\n      \"countWords\",\n      \"countWordsLearned\",\n      \"picture\",\n      \"category\",\n      \"status\",\n      \"source\",\n      \"level\"\n    ]\n  }\n]",
          "request": [
            {
              "subOp": "myAll",
              "type": "user",
              "perPage": 999,
              "sortBy": "created",
              "attrList": {
                "type": "type",
                "id": "id",
                "name": "name",
                "countWords": "cw",
                "countWordsLearned": "cl",
                "wordSetId": "wordSetId",
                "picture": "pic",
                "category": "cat",
                "status": "st",
                "source": "src"
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
        post_response = self.session.post(url, data=params)
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


    # Функция перемещения слова в другой набор (из набора "Слова из интернета")
    def move_word(self, word_set_id, word_id):
        url = 'https://api.lingualeo.com/SetWords'
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
        params = '{"apiVersion":"1.0.1","op":"groupActionWithWords {action: add}","data":[{"action":"add","mode":"move","wordSetId":3,"wordIds":[%s],"dateGroups":[],"filter":{"category":"","status":"","training":null,"search":""},"chunk":1,"valueList":{"globalSetId":3,"wordSetId":%s}}],"userData":{"nativeLanguage":"lang_id_src"},"ctx":{"config":{"isCheckData":true,"isLogging":true}}}' % (word_id, word_set_id)
        options_response = self.session.options(url, headers=options_headers)
        post_response = self.session.post(url, data=params.encode('utf-8'), headers=post_headers)
        return json.loads(post_response.text)


    # Функция перемещения добавленных в Lingualeo слов в нужный набор слов
    def move_word_set(self, word_set_id):
        words, state_count = self.get_words(3), 0
        print("Перемещение слов в нужный набор...", end="")
        while words['wordSet']['countWords'] != 0:
            for elem in words['data'][0]['words']:
                self.move_word(word_set_id, elem['id'])
                state_count = (state_count + 1) % 6
                if state_count == 0:
                    print("\rПеремещение слов в нужный набор...", end="")
                elif state_count == 1:
                    print("\rПеремещение слов в нужный набор ..", end="")
                elif state_count == 2:
                    print("\rПеремещение слов в нужный набор  .", end="")
                elif state_count == 3:
                    print("\rПеремещение слов в нужный набор   ", end="")
                elif state_count == 4:
                    print("\rПеремещение слов в нужный набор.  ", end="")
                elif state_count == 5:
                    print("\rПеремещение слов в нужный набор.. ", end="")
            words = self.get_words(3)
        print("\r                                  ", end="")
        print('\rПеремещение слов завершено!')


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
