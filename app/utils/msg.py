import requests
import json


class Ding(object):
    def __init__(self):
        self.headers = {'content-type': 'application/json;charset=utf-8'}
        self.url = 'https://oapi.dingtalk.com/robot/send?access_token=9d6da20b7e3e596c660b5b6379a2e10f962b823d076c11bbfea3f393bfdcb1cd'
        self.mobiles = []
        self.text = ''
        self.at_all = False
        self.type = 'text'

    def at(self, mobile, at_all=False):
        self.mobiles.append(mobile)
        self.at_all = at_all
        return self

    def remove_at(self, mobile):
        self.mobiles.remove(mobile)
        return self

    def msg(self, msg):
        self.text = msg
        return self

    def msg_type(self, msg_type):
        if msg_type in ['text', 'link']:
            self.type = msg_type
        return self

    def send(self):
        text = self.__build_msg()
        requests.post(self.url, data=text, headers=self.headers)

    def __build_msg(self):
        text = {'msgtype': self.type}
        at = ''.join(['@' + mobile for mobile in self.mobiles])
        if self.type == 'text':
            text['text'] = {'content': at + self.text}
        text['at'] = {'atMobiles': self.mobiles, 'isAtAll': self.at_all}
        return json.dumps(text)
