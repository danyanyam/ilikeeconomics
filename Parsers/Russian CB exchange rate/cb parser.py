#!/usr/bin/env python
# coding: utf-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def get_values(date_b, date_e, VAL_NM_RQ='R01235'):
    urlis = 'http://www.cbr.ru/scripts/XML_dynamic.asp?'
    html_doc = urlopen(urlis + 'date_req1=' + date_b + '&date_req2=' + date_e + '&VAL_NM_RQ=' + VAL_NM_RQ).read()
    soup = BeautifulSoup(html_doc, features="html.parser")
    data = soup.find_all('record')
    records = {}
    for record in data:
        records.update({record['date']: record.text[1:]})
    return records

def clean_frame(records):
    df = pd.DataFrame(data=records.items())
    df.index = df[0]
    df = df.drop([0], axis=1)
    df.columns = ['USD']
    return df

def get_mean_rate(start, end):
    df = clean_frame(get_values(start, end))
    values = df.values
    new = []
    for rate in values:
        new.append(float(rate[0].replace(',', '.')))
    array = np.array(new).mean()
    return array

# Use this function to get mean of rates in given range of time
get_mean_rate('01.01.2013', '01.01.2014')
