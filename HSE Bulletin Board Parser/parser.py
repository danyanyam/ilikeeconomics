
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.hse.ru/ba/economics/students/'

class Parser:
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup(self.url)
        self.headings = self.get_headings(self.soup)
        self.links = self.get_links(self.soup)
        self.date = self.get_date(self.soup)
        self.dataframe = self.get_dataframe(self.headings, self.links, self.date)
        self.new = self.get_n_newest

    def get_soup(self, url):
        html_doc = urlopen(url).read()
        soup = BeautifulSoup(html_doc, features="html.parser")
        return soup

    def get_links(self, soup):
        '''
        :param soup:
        :return list of links:
        '''
        links = []
        divs = soup.find_all('div', 'blackboard-item__cont')
        for html in divs:
            links.append(html.find('a').get('href'))
        return links

    def get_headings(self, soup):
        '''
        :param soup:
        :return list of headings:
        '''
        headings = []
        divs = soup.find_all('div', 'blackboard-item__cont')
        for html in divs:
            headings.append(html.find('a').text)
        return headings

    def get_date(self, soup):
        '''
        :param soup:
        :return list of dates:
        '''
        date = []
        divs = soup.find_all('div', 'blackboard-item__date')
        for html in divs:
            date.append(html.text)
        return date

    def get_dataframe(self, headings, links, date):
        '''
        :param headings:
        :param links:
        :param date:
        :return pandas dataframe:
        '''
        dataframe = pd.DataFrame([headings, links]).T
        dataframe[2] = date
        dataframe = dataframe.rename(columns={0: 'Headings', 1: 'Links', 2: 'Date'})
        dataframe = dataframe[['Date', 'Headings', 'Links']]
        return dataframe

    def get_n_newest(self, n=5):
        '''
        :param n:
        :return n rows of dataframe:
        '''
        dataframe = self.dataframe
        return dataframe.iloc[:n, :]



parser = Parser(url)
headings = parser.headings
links = parser.links
date = parser.date
print(parser.dataframe)






