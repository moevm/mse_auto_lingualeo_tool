from http.cookiejar import CookieJar
import json
import urllib.parse as urlp
import urllib.request as urlreq


# Класс для работы с сервисом Lingualeo
class lingualeo_service:
    # Конструтор от email-а и пароля, используемые при авторизации на Lingualeo 
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.cookie_jar = CookieJar()


    # Авторизация в Lingauleo, необходимое для дальнейшей работы
    def auth(self):
        url = "http://api.lingualeo.com/api/login"
        values = {
            "email": self.email,
            "password": self.password
        }
        return self.make_request(url, values)


    # Функция добавления одного слова в набор слов Lingualeo
    def add_word(self, word, translate, context):
        url = "http://api.lingualeo.com/addword"
        values = {
            "word": word,
            "tword": translate,
            "context": context,
        }
        return self.make_request(url, values)


    # Функция отправки запроса на Lingualeo (необходимо пофиксить)
    def make_request(self, url, values):
        data = urlp.urlencode(values)
        opener = urlreq.build_opener(urlreq.HTTPCookieProcessor(self.cookie_jar))
        req = opener.open(url, data.encode())
        return json.loads(req.read())
