from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import re
import time
import pandas as pd

#setting chrome driver path
# Init:
gecko_path = 'C:/Users/ASUS/Python Folder/Drivers/geckodriver.exe'
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser)

url = 'https://www.ted.com/talks?page=1'

#calling the website url
driver.get(url)

# setting boolean parameter for page limit
page_limit = False

if page_limit == True:
    max_pages = 3
else: max_pages = 100



# declaring lists to store scraped data
video_titles = []
speaker = []
date = []
video_links=[]





for i in range(2,max_pages+1):
    

    names = driver.find_elements(By.XPATH,'//div[@class="media__message"]/h4[2]/a')
    for name in range(len(names)):
        video_titles.append(names[name].text) 


    course = driver.find_elements(By.XPATH,'//div[@class="media__message"]/h4[1]')
    for cs in range(len(course)):
        speaker.append(course[cs].text)


    sectros = driver.find_elements(By.XPATH,'//div[@class="meta"]/span/span')
    for sectro in range(len(sectros)):
        date.append(sectros[sectro].text)

    Links = driver.find_elements(By.XPATH,'//div[@class="media__message"]/h4[2]/a')
    for link in range(len(Links)):
        video_links.append(Links[link].get_attribute('href'))

     
    # using time.sleep for a slight delay in code to interact and find all the elements
    time.sleep(1)
    driver.get('https://www.ted.com/talks?page='+str(i))
# creating a dictionary to store the scraped data in previous step
data_dictionary = {'Name': video_titles, 'Course': speaker, 'Sector': date, 'Links' : video_links }

# storing the scraped data in csv file
#dataframe = pd.DataFrame(data_dictionary)
#dataframe.to_csv('data.csv', mode='a', index=False, header=False, encoding="cp1252")
df = pd.DataFrame.from_dict(data_dictionary, orient='index')
df = df.transpose()
df = df.sort_values(by=['Name'], ascending=True)
df.to_csv('C:/Users/ASUS/Python Folder/websc/data_selenium.csv', index=False)



# closing the driver instance and browser window
driver.quit()
