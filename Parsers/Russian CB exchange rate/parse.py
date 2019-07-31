# This code is accomplished by dvbuchko@edu.hse.ru
# Contact me by e-mail in order you have any questions

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import time
import os

def get_all_codes():
    url = 'http://www.cbr.ru/scripts/XML_valFull.asp'
    # Ссылка на API cbr, к которому нео  бходимо обращаться с запросами
    # VAL_NM_RQ='RXXXX' - таким образом отображается валютная пара YYYY/RUB
    
    html_doc = urlopen(url)
    soup = BeautifulSoup(html_doc, features="html.parser")
    all_codes = soup.find_all('item')
    codes = {}
    for i in all_codes:    
        if i.find('iso_char_code').text != '':
            codes.update({i.find('iso_char_code').text: i['id']})
    return codes

def get_values(date_b, date_e, VAL_NM_RQ='R01235'):
    
    # Ссылка на API cbr, к которому нео  бходимо обращаться с запросами
    # VAL_NM_RQ='R01235' - таким образом отображается валютная пара USD/RUB
    
    url = 'http://www.cbr.ru/scripts/XML_dynamic.asp?'
    while True:
        try:
            html_doc = urlopen(url + 'date_req1=' + date_b + '&date_req2=' + date_e + '&VAL_NM_RQ=' + VAL_NM_RQ).read()
        except:
            continue
        break
        
    soup = BeautifulSoup(html_doc, features="html.parser")
    data = soup.find_all('record')
    
    # Преобразуем полученные данные в словарь
    records = {}
    for record in data:
        records.update({record['date']: record.text[1:]})
    return records

def choose_cur():
    
    '''Предлагает пользователю выбать валюту'''
    
    codes = get_all_codes()
    codes = dict(sorted(codes.items()))
    answer = str(input('\nВведите аббревиатуру валюты, которая вас интересует. Вы также можете получить' +
                       ' список всех доступных валют, если введете слово "список".\n')).upper()
    if answer.lower() == 'список':
        for i, cur in enumerate(codes):
            print(i, '-', cur)
        answer = str(input('\nВведите аббревиатуру валюты, которая вас интересует.\n')).upper()
        
    while answer not in codes.keys():
        answer = input('\nКажется ЦБ не предоставляет курс для введенной валюты, попробуйте проверить правильность котировки или вызовите '+
              'список доступных котировок командой "список".\n').upper()
        
        if answer.lower() == 'список':
            for i, cur in enumerate(codes):
                print(i, '-', cur)
            answer = str(input('\nВведите аббревиатуру валюты, которая вас интересует.\n')).upper()
            print(answer)
    return (codes[answer], answer)

def get_dfval(start, end, VAL_NM_RQ):
    data = get_values(start, end, VAL_NM_RQ)
    list = []
    for value in data.values():
        value = float(value.replace(",", "."))
        list.append(value)
    df_val = pd.DataFrame(list, index=data.keys())
    
    new_list = []
    for date in df_val.index:
        month = date[3:5]
        day = date[0:2]
        year = date[-4:]
        new_list.append(year + '-' + month + '-' + day)
    df_val.index = new_list
    
    return df_val
    

def gui():
    start = input('\nВведите начало финансового года в формате dd.mm.yyyy:\n')
    while len(start) != 10:
        start = input('\nВведите КОРРЕКТНОЕ начало финансового года в формате dd.mm.yyyy:\n')
    end = input('\nВведите окончание финансового года в формате dd.mm.yyyy:\n')
    
    if int(start[-4:]) > int(end[-4:]):
        print("\nДаты введены некорректно: начало финансового года не может быть позже его завершения.\n")
        start = input('\nВведите начало финансового года в формате dd.mm.yyyy:\n')
        while len(start) != 10:
            start = input('\nВведите КОРРЕКТНОЕ начало финансового года в формате dd.mm.yyyy:\n')
        end = input('\nВведите окончание финансового года в формате dd.mm.yyyy:\n')
        while len(end) != 10:
            end = input('\nВведите КОРРЕКТНОЕ начало финансового года в формате dd.mm.yyyy:\n')
        
    
    VAL_NM_RQ = choose_cur()
    
    # Заменяем запятые на точки и создаем датафрейм
    df_val = get_dfval(start, end, VAL_NM_RQ[0])
    
    # Объединим датафреймы и заполним пропуски данными, полученными раннее
    if df_val.empty == False:
        main = get_empty_df(start, end).join(df_val).fillna(method='ffill').copy()
    # Возможна ситуация, когда на запрошенную дату вообще нет котировок, в таком случае нам необходимо будет
    # выгрузить данные за последнюю неделю предыдущего года и использовать эти данные вместо пропусков
    else:
        main = get_empty_df(start, end)
        time.sleep(0.5)
        start = '20/12/' + str(int(start[-4:]) - 1)
        end = '31/12/' + str(int(end[-4:]) - 1)
        
        df_prev = get_dfval(start, end, VAL_NM_RQ[0])
        df_main_prev = get_empty_df(start, end).join(df_prev).fillna(method='ffill').copy()
        main = main.append({0: df_main_prev.iloc[-1, -1]}, ignore_index=True)
        main = main.fillna(method='ffill')

    
    # Если курс на первое число указанной даты не указан, то подгрузим данные за год до указанного
    # и достанем его оттуда
    if str(main.iloc[0, 0]) == 'nan':
        time.sleep(0.7)
        start = start[:-4] + str(int(start[-4:]) - 1)
        end = end[:-4] + str(int(end[-4:]) - 1)
        
        df_prev = get_dfval(start, end, VAL_NM_RQ[0])
        df_main_prev = get_empty_df(start, end).join(df_prev).fillna(method='ffill').copy()
        main.iloc[0, 0] = df_main_prev.iloc[-1, -1]
        main = main.fillna(method='ffill')
    print('\n', '------' * 15, sep='')
    print('Средний курс ' + VAL_NM_RQ[1] +'/RUB ' + 'за указанный промежуток времени составил: ', float(main.mean()))
    print('\nКоличество котировок за указанный промежуток времени составило: ', len(main))
    print('------' * 15)
    print('\nНажмите ENTER, чтобы завершить, или используйте следующие команды:\n')
    print('1. "еще" - чтобы запустить алгоритм заново. ')
    print('2. "котировки" - чтобы выгрузить котировки за указанный промежуток времени в excel в csv формате')
    print('3. "исходный код" - чтобы получить ссылку на исходный код программы\n')
    answer = input()
    if answer.lower() == "еще":
        gui()
    if answer.lower() == "котировки":
        print('\n...Сохранение...\n')
        main.to_csv('rates.csv')
        print('Сохраненный файл находится в ',  os.getcwd(), '\\', sep="")
        _ = input('Сохранение прошло успешно. Нажмите ENTER, чтобы выйти.\n')
    if answer.lower() == "исходный код":
        print('https://github.com/danyanyam/ihateeconomics/blob/master/Parsers/Russian%20CB%20exchange%20rate/cb%20parser.py')
        _ = input('\nНажмите ENTER, чтобы выйти.\n')
		
        
    
def get_empty_df(start, end):
    # Создаем пустой датафрейм с индексами, лежащими в диапазоне наших дат
    month = start[3:5]
    day = start[0:2]
    year = start[-4:]
    start = year + '-' + month + '-' + day
    
    month = end[3:5]
    day = end[0:2]
    year = end[-4:]
    end = year + '-' + month + '-' + day

    datelist = pd.date_range(start, end).tolist() 
    df = pd.DataFrame(index=datelist)
    return df

gui()
