from bs4 import BeautifulSoup as BS
from urllib import request as re
from lxml import etree
import time
import pandas as pd

# setting boolean parameter for page limit
page_limit = False

if page_limit:  # Change to True if you want to limit the number of pages
    max_pages = 10
else:
    max_pages = 100

# declaring lists to store scraped data
video_titles = []
speaker = []
date = []
video_links=[]
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
# iterating over first 100 pages to scrap required data
for i in range(1, max_pages+1):
    if i%10==0:
        time.sleep(1)
    print('\n',i)
    url = 'https://www.ted.com/talks?page='+str(i)
    req = re.Request(url, headers=headers)
    html = re.urlopen(req)
    bs = BS(html.read(), 'html.parser')


    t1 = bs.find_all('h4', {'class':'h12 talk-link__speaker'})
    for elem in t1:
        speaker.append(elem.text.strip())
    talk_elements = bs.find_all('div', class_='col')
    for talk_element in talk_elements:
        title_element = talk_element.find('h4', class_='h9')
        if title_element:
            video_titles.append(title_element.text.strip())
            link_element = talk_element.find('a', class_='ga-link', href=True)
            if link_element:
                video_links.append("https://www.ted.com" + link_element['href'])

    dt=bs.find_all('span', {'class':'meta__val'})
    for elem in dt:
        date.append(elem.text.strip())

# creating a dictionary to store the scraped data in previous step
data_dictionary = {'Title': video_titles, 'Speaker': speaker, 'Date Posted': date, 'Link' : video_links }



df = pd.DataFrame.from_dict(data_dictionary, orient='index')
df = df.transpose()
df = df.sort_values(by=['Title'], ascending=True)
df.to_csv('C:/Users/ASUS/Python Folder/data_bsoup.csv',index = False)
