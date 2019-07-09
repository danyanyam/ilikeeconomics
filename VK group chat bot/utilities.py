import requests
token = 'f0a0d43e603ea40c288a62d0d51052d84cb587e170efbcec960c905e74d7461636695558a46c380a1b9f7'
tech_tocken = '67ab4b4067ab4b4067ab4b402e67c03f20667ab67ab4b403ab08188299fc0180eee0b9d'

# print('---- https://api.vk.com/method/METHOD_NAME?PARAMETERS&access_token=ACCESS_TOKEN&v=V ----')
def random_wall_photo(token):

    '''
    :param token: string
    :return: string, формата необходимого для отправки в диалоге типа <TYPE><OWNER_ID>_<PHOTO_ID>
    '''
    from random import randint
    url = 'https://api.vk.com/method/'
    v = '5.101'
    group_id = '-97121274'
    number = randint(1, 297)
    method = 'photos.get'
    response = requests.get(url+method,
                            params={
                                'owner_id': group_id,
                                'album_id': 'wall',
                                'rev': 1,
                                'count': 300,
                                'access_token': token,
                                'v': v
                            })
    image_id = response.json()['response']['items'][number]['id']
    owner_id = response.json()['response']['items'][number]['owner_id']
    attachment = 'photo'+str(owner_id)+"_"+str(image_id)
    return attachment



def upload_photo(image, peer_id, token):

    '''
    :param image: string, название картинки в папке с кодом
    :param peer_id: string, адрес, кому отсылается сообщение
    :param token: string, ключ доступа
    :return: string, формата необходимого для отправки в диалоге типа <TYPE><OWNER_ID>_<PHOTO_ID>
    '''

    url = 'https://api.vk.com/method/'
    v = '5.101'
    method = 'photos.getMessagesUploadServer'
    image = {'photo': open(image, 'rb')}

    # Получаем ссылку на загрузку фото
    response = requests.get(url + method,
                            params={
                                'peer_id': peer_id,
                                'access_token': token,
                                'v': v
                            })
    upload_url = response.json()['response']['upload_url']

    response = requests.post(upload_url, files=image)
    params = {'server': response.json()['server'],
              'photo': response.json()['photo'],
              'hash': response.json()['hash'],
              'access_token': token,
              'v': v
              }
    method1 = 'photos.saveMessagesPhoto'
    response = requests.get(url + method1, params=params)
    msg = response

    photo_id = msg.json()['response'][0]['id']
    owner_id = msg.json()['response'][0]['owner_id']
    attachment = 'photo' + str(owner_id) + '_' + str(photo_id)
    return attachment


def get_timetable(tech_token):
    '''
    :param tech_token: string
    :return: i - количество объектов в закрепе
             answers - массив с названиями документов и ссылками на них
             mem - string, ссылка на фотомем
    '''
    method = 'wall.get'
    url = 'https://api.vk.com/method/'
    v = '5.101'
    response = requests.post(url+method,
                             params={
                                 'access_token': tech_token,
                                 'v': v,
                                 'owner_id': '-16757548',
                                 'count': 1,
                             })
    attaches = response.json()['response']['items'][0]['attachments']
    for i in range(len(attaches)):
        answers = []
        mem = []
        for i in range(len(attaches)):
            if i > 0:
                title = attaches[i]['doc']['title'][:-4] + '\t'
                url = attaches[i]['doc']['url'] + '\n'
                answers.append(title)
                answers.append(url)
            elif i == 0:
                media_id = attaches[0]['photo']['id']
                owner_id = attaches[0]['photo']['owner_id']
                mem = 'photo' + str(owner_id) + "_" + str(media_id)
        return i, answers, mem



