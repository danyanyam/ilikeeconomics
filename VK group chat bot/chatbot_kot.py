from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import pandas as pd
from utilities import random_wall_photo, get_timetable


token = 'f0a0d43e603ea40c288a62d0d51052d84cb587e170efbcec960c905e74d7461636695558a46c380a1b9f7'
tech_token = '67ab4b4067ab4b4067ab4b402e67c03f20667ab67ab4b403ab08188299fc0180eee0b9d'
group_id = '97121274'
url = 'https://api.vk.com/method/'
v = '5.101'
vk = vk_api.VkApi(token=token)

data = pd.read_csv('cat.csv')['url']
upload = vk_api.VkUpload(vk)
vk._auth_token()
vk.get_api()
longpoll = VkBotLongPoll(vk, group_id)
keyboard = open('mainmenu_keyboard.json', 'r', encoding='UTF-8').read()
keyboard_1 = open('1_timetable_keyboard.json', 'r', encoding='UTF-8').read()
keyboard_2 = open('2_timetable_keyboard.json', 'r', encoding='UTF-8').read()


while True:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.object.peer_id == event.object.from_id:
                print(event.object.text)
                if event.object.text.lower() == "привет" or event.object.text.lower() == 'ку'\
                        or event.object.text.lower() == 'привет!' or event.object.text.lower() == 'здравствуй' \
                        or event.object.text.lower() == 'здравствуйте':

                    print('----- Приветствие -----')
                    print(event)
                    print(event.object.from_id)
                    vk.method("messages.send", {"peer_id": event.object.peer_id,
                                                "message": 'Привет, любитель котов! Рад видеть тебя у нас в гнёздышке. '
                                                           'Если вдруг ты захочешь посмотреть котиков, просто отправь '
                                                           'слово "кот" в ответ на это сообщение.',
                                                "attachment": random_wall_photo(tech_token),
                                                'keyboard': keyboard,
                                                "random_id": 0})

                if event.object.text.lower() == "зиг":
                    print('----- Шутка -----')
                    vk.method("messages.send", {"peer_id": event.object.peer_id,
                                                "message": 'дима успокойся',
                                                "random_id": 0})

                if event.object.text.lower() == "ира + дима" or event.object.text.lower() == "ира+дима":
                    vk.method("messages.send", {"peer_id": event.object.peer_id,
                                                "message": '❤',
                                                "random_id": 0})

                if event.object.text.lower() == "кот":
                    print('----- Фото -----')
                    vk.method("messages.send", {"peer_id": event.object.peer_id,
                                                "message": 'Напиши слово "кот", чтобы увидеть еще!',
                                                "attachment": random_wall_photo(tech_token),
                                                "random_id": 0})

                if event.object.text.lower() == "расписание автобуса до дубков":
                    print('---- Расписание ----')
                    i, tables, mem = get_timetable(tech_token)
                    if i == 1:
                        vk.method("messages.send", {"peer_id":  event.object.peer_id,
                                                    "message": 'Что вам показать: студсоветский мем или расписание?',
                                                    "random_id": 0,
                                                    "keyboard": keyboard_1})
                    if i == 2:
                        vk.method("messages.send", {"peer_id": event.object.peer_id,
                                                    "message": 'Что вам показать: студсоветский мем или расписание?',
                                                    "random_id": 0,
                                                    "keyboard": keyboard_2})

                if event.object.text.lower() == "посмотреть расписание.":
                    vk.method("messages.send", {"peer_id": event.object.peer_id,
                                                "message": tables[0]+'\n'+tables[1],
                                                "random_id": 0})

                if event.object.text.lower() == "посмотреть расписание":
                    vk.method("messages.send", {"peer_id": event.object.peer_id,
                                                "message": tables[0] + '\t' + tables[1]+'\n'+tables[2] + '\t' + tables[3],
                                                "random_id": 0})

                if event.object.text.lower() == "посмотреть мем":
                    vk.method("messages.send", {"peer_id": event.object.peer_id,
                                                "message": 'Вот тебе мемасик!',
                                                'attachment': mem,
                                                "random_id": 0})

                if event.object.text.lower() == "вернуться в главное меню":
                    vk.method("messages.send", {"peer_id": event.object.peer_id,
                                                "message": 'Привет, любитель котов! Рад видеть тебя у нас в гнёздышке. '
                                                           'Если вдруг ты захочешь посмотреть котиков, просто отправь '
                                                           'слово "кот" в ответ на это сообщение.',
                                                "attachment": random_wall_photo(tech_token),
                                                'keyboard': keyboard,
                                                "random_id": 0})




