import requests

class Pingmeen:
    def __init__(self, token):
        self.token = token
        response = self.__server_query('validate_token')
        if response != 'true':
            raise Exception
        
    def finish(self):
        self.__server_query('send_message')
        
    def __server_query(self, method):
        url = 'http://2kolobka.pro/nikita/pingmeen/'
        return requests.get(url + method + '.php?token=' + self.token).text