"""
Название: Play in bots ( Игра в ботах )
Используемые библиотеки: collections, time, requests, vk_api, bs4
Автор: vk.com/rym9n
"""

from collections import Counter
from time import sleep

import requests
import vk_api
from bs4 import BeautifulSoup
from vk_api.longpoll import VkEventType, VkLongPoll


class Civilization(object):
    """Бот угадывающий слова в игре https://vk.com/club175604722"""
    def __init__(self, bot_peer_id, token, time_sleep=10):
        self.BOT_PEER_ID = bot_peer_id
        self.BOT_ID = -175604722
        self.TIME_SLEEP = time_sleep
        self.TOKEN = token
        self.VK = vk_api.VkApi(token=self.TOKEN)
        self.LONGPOLL = VkLongPoll(self.VK)
        self.SESSION_API = self.VK.get_api()

    @staticmethod
    def sanitize(text_):
        """Функция редактирует Counter по алфавиту"""
        yield from (ch.lower() for ch in text_.lower() if ch.isalpha())

    def send_message(self, peer_id, message):
        """Отправка сообщения пользователю/беседе с некоторой задержкой заданной в TIME_SLEEP"""
        sleep(self.TIME_SLEEP)
        self.SESSION_API.messages.send(peer_id=peer_id,
                                       random_id=0,
                                       message=message)

    def find_words(self, peer_id, word):
        """Поиск подходящих по параметрам слов"""
        words_return = [word]
        url = f'https://xn--b1algemdcsb.xn--p1ai/anagram/search?query={word}'
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        new_word = None
        for new_word in soup.find_all(class_='dict-section'):
            if str(len(word)) in str(new_word.h4).replace('h4', ''):
                break
        try:
            for text in new_word.find_all('a'):
                if Counter(text.getText()) == Counter(self.sanitize(word)):
                    words_return.append(text.getText())
            self.send_message(peer_id, 'ответ ' + words_return[0].lower())
            words_return.pop(0)
            return words_return
        except AttributeError:
            self.send_message(peer_id, 'другое слово')
        except IndexError:
            self.send_message(peer_id, 'другое слово')

    def run(self):
        words = []
        while True:
            try:
                self.send_message(self.BOT_PEER_ID, 'слово')
                for event in self.LONGPOLL.listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        if event.peer_id == self.BOT_PEER_ID and event.user_id == self.BOT_ID:
                            if len(event.text) < 3:
                                self.send_message(event.peer_id, 'другое слово')
                            elif 'слово' in event.text.lower():
                                find_word = event.text.lower().split(': ')[1]
                                words = self.find_words(event.peer_id, find_word)
                            elif not words:
                                self.send_message(event.peer_id, 'другое слово')
                            elif 'ответ неверный!' in event.text.lower():
                                self.send_message(event.peer_id, 'ответ ' + words[0].lower())
                                words.pop(0)
                            elif 'ответ принят' in event.text.lower():
                                self.send_message(event.peer_id, 'слово')
            except vk_api.Captcha:
                sleep(60)
            except requests.ConnectionError:
                continue
