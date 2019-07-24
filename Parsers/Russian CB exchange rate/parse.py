#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

start = '01/01/2010' 
end = '31/12/2010'

def get_values(date_b, date_e, VAL_NM_RQ='R01235'):
    
    # Ссылка на API cbr, к которому необходимо обращаться с запросами
    # VAL_NM_RQ='R01235' - таким образом отображается валютная пара USD/RUB
    
    url = 'http://www.cbr.ru/scripts/XML_dynamic.asp?'
    html_doc = urlopen(url + 'date_req1=' + date_b + '&date_req2=' + date_e + '&VAL_NM_RQ=' + VAL_NM_RQ).read()
    soup = BeautifulSoup(html_doc, features="html.parser")
    data = soup.find_all('record')
    
    # Преобразуем полученные данные в словарь
    records = {}
    for record in data:
        records.update({record['date']: record.text[1:]})
    return records

def get_mean(start, end):
    
    # Создаем пустой датафрейм с индексами, лежащими в диапазоне наших дат
    datelist = pd.date_range(start, end).tolist() 
    df = pd.DataFrame(index=datelist)

    # Получаем словарь парснутых данных
    values = get_values(start, end)

    # Поменяем decimal separator с "," на "."
    list = []
    for value in values.values():
        value = float(value.replace(",", "."))
        list.append(value)

    # Создадим датафрейм с полученными данными
    df_val = pd.DataFrame(list, index=values.keys())

    # Объединим датафреймы и заполним пропуски данными, полученными раннее
    main = df.join(df_val).fillna(method='ffill').copy()

    # На случай, если первое значение курса валют осталось NaN, заполним его данными с будущего значения, чтобы не усложнять задачу
    main = main.fillna(method='bfill')

    # Посчитаем среднее значение курса валют
    return main

def main():
    print()
    start = input('Введите начало финансового года в формате dd.mm.yyyy:\n')
    end = input('\nВведите окончание финансового года в формате dd.mm.yyyy:\n')
    print('\nСредний курс доллара за указанный промежуток времени составил: ', get_mean(start, end).mean().item())
    print('\nКоличество котировок за указанный промежуток времени составило: ', len(get_mean(start, end)))
    answer = input('\nНажмите ENTER, чтобы завершить, или введите слово "еще", чтобы продолжить')
    if answer == "еще":
        main()
    
if __name__ == '__main__':
    main()


# In[ ]:




