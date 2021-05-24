import requests
import pandas as pd
from bs4 import BeautifulSoup


HEADERS = {'User-agent': 'Mozilla/5.0'}


def get_html(url, params=None):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('ul', class_='menu-h')
    if pagination:
        max_page = 1
        links = pagination.find_all('a')
        for a in links:
            try:
                if int(a.text) > max_page:
                    max_page = int(a.text)
            except:
                pass
        return max_page
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='pl-item-wrapper')
    parts = []
    for item in items:
        finite_price = item.find('span', class_='price')
        if finite_price:
            finite_price = item.find('span', class_='price').get_text(strip=True)
        else:
            finite_price = 'None'
        parts.append({
            'title': item.find('div', class_='summary').get_text(strip=True),
            'offers': finite_price,

        })
    return parts


def parse():
    URL = input('Entrt URL: ')
    URL = URL.strip()
    html = get_html(URL)

    if html.status_code == 200:
        parts = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Parsing page № {page} in {pages_count}')
            html = get_html(URL, params={'page': page})
            parts.extend(get_content(html.text))
        return parts
    else:
        print('Error')


if __name__ == '__main__':
    list = parse()
    df_ofer = pd.DataFrame(list)
    df_ofer.to_excel('./result.xlsx', sheet_name='Price')

