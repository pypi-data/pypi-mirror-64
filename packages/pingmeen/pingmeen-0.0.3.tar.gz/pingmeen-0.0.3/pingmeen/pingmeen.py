import requests

class Pingmeen:
    def __init__(self, token):
        self.token = token
        
    def finish(self):
        url = 'http://2kolobka.pro/nikita/pingmeen/send_message.php'
        requests.get(url + '?token=' + self.token)
        