import scrapy
import pandas as pd

# Set the page limit flag
page_limit = True

# Define the number of pages to scrape
if page_limit:
    pages = 3
else:
    pages = 100

# Define the Spider class
class TedSpider(scrapy.Spider):
    name = "ted"  # Name of the spider
    allowed_domains = ['ted.com']  # Domains that the spider is allowed to crawl
    # Generate the start URLs based on the number of pages
    start_urls = [f'https://www.ted.com/talks?page={i}' for i in range(1, pages + 1)]

    # The main parsing function
    def parse(self, response):
        # Extract video titles from the page
        video_titles = [text.strip() for text in response.xpath('//div[@class="media__message"]/h4[2]/a/text()').extract()]
        
        # Extract speaker names from the page
        speaker = response.xpath('//div[@class="media__message"]/h4[1]/text()').extract()
        
        # Extract dates from the page
        date = [text.strip() for text in response.xpath('//div[@class="meta"]/span/span/text()').extract()]
        
        # Extract links to the videos from the page
        links = response.xpath('//div[@class="media__message"]/h4[2]/a/@href').extract()
        
        # Construct full links for the videos
        video_links = ["https://www.ted.com" + link for link in links]
        
        # Create a dictionary to hold the scraped data
        data_dictionary = {'Title': video_titles,
                           'Speaker': speaker,
                           'Date Posted': date,
                           'Link': video_links}
        
        # Create a DataFrame from the data dictionary
        df = pd.DataFrame(data_dictionary)
        
        # Sort the DataFrame by title in ascending order
        df = df.sort_values(by=['Title'], ascending=True)
        
        # Append the data to a CSV file
        df.to_csv('C:/Users/ASUS/Python Folder/data_scrapy.csv', mode='a', index=False)

# Create an instance of the CrawlerProcess and start the Spider
process = scrapy.crawler.CrawlerProcess()
process.crawl(TedSpider)
process.start()
