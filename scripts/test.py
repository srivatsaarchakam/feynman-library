from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Specify the correct path to your chromedriver
service = Service('/System/Volumes/Data/Users/srivatsakrishnamurthy/Documents/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)

try:
    driver.get('http://google.com')
    print("WebDriver is running properly.")
finally:
    driver.quit()