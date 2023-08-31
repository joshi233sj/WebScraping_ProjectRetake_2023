import scrapy
import pandas as pd
page_limit = False

if page_limit:
    pages = 3
else:
    pages = 100

class TedSpider(scrapy.Spider):
    name = "ted"
    allowed_domains = ['ted.com']
    start_urls = [f'https://www.ted.com/talks?page={i}' for i in range(1, pages + 1)]
    

    def parse(self, response):
        video_titles = [text.strip() for text in response.xpath('//div[@class="media__message"]/h4[2]/a/text()').extract()]
        speaker = response.xpath('//div[@class="media__message"]/h4[1]/text()').extract()
        date = [text.strip() for text in response.xpath('//div[@class="meta"]/span/span/text()').extract()]
        links = response.xpath('//div[@class="media__message"]/h4[2]/a/@href').extract()
        video_links=[]
        for link in links:
            video_links.append("https://www.ted.com" + link)
        data_dictionary = {'Title': video_titles,
                           'Speaker': speaker,
                           'Date Posted': date,
                           'Link': video_links}
        df = pd.DataFrame(data_dictionary)
        df = df.sort_values(by=['Title'], ascending=True)
        df.to_csv('C:/Users/ASUS/Python Folder/data_scrapy.csv',mode='a', index=False)
