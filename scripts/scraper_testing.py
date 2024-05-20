from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os

# Setup Chrome WebDriver
service = Service('/System/Volumes/Data/Users/srivatsakrishnamurthy/Documents/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)

# Main URL of the Feynman Lectures
main_url = "https://www.feynmanlectures.caltech.edu"

# Directory for saving data
data_directory = '/System/Volumes/Data/Users/srivatsakrishnamurthy/Documents/dev/FeynmanLibrary/data'
os.makedirs(data_directory, exist_ok=True)

# List of chapters to scrape
chapters = ["I_01", "I_02", "I_03", "I_04", "I_05", "I_06" ]  # Example chapters, adjust as necessary

all_chapters_content = []

for chapter in chapters:
    chapter_url = f"{main_url}/{chapter}.html"
    print(f"Accessing {chapter_url}")
    driver.get(chapter_url)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.para')))


    # Collect content in order maintaining order of elements
    content_elements = []
    paragraph_elements = driver.find_elements(By.CSS_SELECTOR, 'div.para')
    image_elements = driver.find_elements(By.CSS_SELECTOR, 'img')
    math_elements = driver.find_elements(By.CSS_SELECTOR, 'span.MathJax')

    for element in paragraph_elements:
        text = ' '.join(element.text.split())
        content_elements.append({'type': 'text', 'data': element.text})

    for element in image_elements:
        img_src = element.get_attribute('src')
        if img_src and img_src.startswith('http'):  # Check if img_src is not None and starts with 'http'
            content_elements.append({'type': 'image', 'data': img_src})
        elif img_src:  # Handle relative URLs only if img_src is not None
            img_url = main_url + img_src
            content_elements.append({'type': 'image', 'data': img_url})

    for element in math_elements:
        math_content = element.get_attribute('data-latex') or element.text
        content_elements.append({'type': 'math', 'data': math_content})

    # Structure the chapter data
    formatted_chapter_data = {
        'input': chapter,
        'output': content_elements
    }
    all_chapters_content.append(formatted_chapter_data)

# Close the browser after scraping
driver.quit()

# Save all data into a JSON file
json_filename = os.path.join(data_directory, 'feynman_lectures_data.json')
with open(json_filename, 'w') as f:
    json.dump(all_chapters_content, f, indent=4)
