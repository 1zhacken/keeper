import requests
from lxml import html
import time
import re

token = '1228561106:AAGu4jlSZCw2OllRsAIfScCRt3RcuEI8Aws'
pages = ['https://muzline.ua/fender-squier-classic-vibe-70s-jaguar-lrl-black/']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
last_price = []

for p in pages:
    last_price.append(0)

while True:
    try:
        for i in range(len(pages)):
            content = requests.get(pages[i], headers=headers).text
            tree = html.fromstring(content)
            price = tree.xpath('//p[@class="price-new"]')[0].text
            if price != last_price[i]:
                name = re.findall(r'[a-zA-Z0-9 ]+', tree.xpath('//title')[0].text)[0]
                r = requests.get('''https://api.telegram.org/bot%s/sendMessage?chat_id=401967130&parse_mode=Markdown&text=изменение цены!
[%s](%s):+%s -> %s!''' % (token, name, pages[i], last_price[i], price))
                last_price[i] = price
            print('success')

    except Exception as e:
        requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=401967130&text=there are error... %s' % (token, e))
        print('oops... %s' % e)

    time.sleep(14400)
    #time.sleep(30)