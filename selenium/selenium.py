from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

# Set the path to the geckodriver (Firefox driver)
gecko_path = 'C:/Users/ASUS/Python Folder/Drivers/geckodriver.exe'

# Initialize the geckodriver service
service = Service(gecko_path)

# Configure options for Firefox driver
options = webdriver.firefox.options.Options()
options.headless = False  # Set to True if you want to run the browser in headless mode

# Initialize the Firefox driver with the service and options
driver = webdriver.Firefox(options=options, service=service)

# URL of the website to scrape
url = 'https://www.ted.com/talks?page=1'

# Load the website
driver.get(url)

# Set the page limit flag
page_limit = False

if page_limit:
    max_pages = 3
else:
    max_pages = 100

# Lists to store scraped data
video_titles = []
speaker = []
date = []
video_links = []

# Loop through pages to scrape data
for i in range(2, max_pages + 1):
    time.sleep(1)
    
    # Extract video titles
    names = driver.find_elements(By.XPATH, '//div[@class="media__message"]/h4[2]/a')
    for name in names:
        video_titles.append(name.text)
    
    # Extract speaker names
    course = driver.find_elements(By.XPATH, '//div[@class="media__message"]/h4[1]')
    for cs in course:
        speaker.append(cs.text)
    
    # Extract dates
    sectros = driver.find_elements(By.XPATH, '//div[@class="meta"]/span/span')
    for sectro in sectros:
        date.append(sectro.text)
    
    # Extract video links
    Links = driver.find_elements(By.XPATH, '//div[@class="media__message"]/h4[2]/a')
    for link in Links:
        video_links.append(link.get_attribute('href'))
    
    # Navigate to the next page
    driver.get('https://www.ted.com/talks?page=' + str(i))

# Create a dictionary to store the scraped data
data_dictionary = {'Name': video_titles, 'Speaker': speaker, 'Date': date, 'Links': video_links}

# Create a DataFrame from the dictionary
df = pd.DataFrame.from_dict(data_dictionary)

# Sort the DataFrame by video name
df = df.sort_values(by=['Name'], ascending=True)

# Save the DataFrame to a CSV file
df.to_csv('data_selenium.csv', index=False)

# Close the driver instance and browser window
driver.quit()
