from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import datetime as dt


def pars_item(strict_template, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    dict_data = dict.fromkeys(strict_template)
    dict_data['title'] = soup.find('h1').text
    dict_data['url'] = url
    data_text = soup.find('time')['datetime']
    dict_data['data'] = dt.datetime.fromisoformat(data_text[:10])
    dict_data['writer_name'] = soup.find('div', attrs={'itemprop': 'author'}).text
    return dict_data


bd_url = 'mongodb://localhost:27017/'

client = MongoClient(bd_url)
db = client['lesson3']
collection = db['geek_post']

strict_template = ('title', 'data', 'writer_name', 'url')
ends_urls = []
list_result = []
domain = 'https://geekbrains.ru'
start_url = '/posts'

dx = 1
while start_url:
    response = requests.get(domain + start_url)
    soup = BeautifulSoup(response.text, 'lxml')
    for child in soup.findAll('a', attrs='post-item__title h3 search_text'):
        if child['href']:
            if child['href'] in ends_urls:
                continue
        ends_urls.append(child['href'])
        list_result.append(pars_item(strict_template, domain + child['href']))
    tmp = soup.find_all('a', attrs={'rel': 'next'})
    if tmp[-1].text == '›':
        start_url = tmp[-1]['href']
    else:
        break
    print(dx, start_url)
    dx += 1

collection.insert_many(list_result)

print(1)
