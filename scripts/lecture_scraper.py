from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import certifi
import json
import time
import re
import os

# chrome webdriver setup
service = Service('/System/Volumes/Data/Users/srivatsakrishnamurthy/Documents/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)

# main url where all of the content is coming from
main_url = "https://www.feynmanlectures.caltech.edu"

# directory to save images
image_directory = '../data/images'
os.makedirs(image_directory,exist_ok=True)

# list of all chapters
chapters = ["I_01", "I_02", "I_03", "I_04", "I_05", "I_06", "I_07", "I_08", "I_09", "I_10", "I_11", "I_12", "I_13", "I_14", "I_15", "I_16", "I_17", "I_18", "I_19", 
            "I_20", "I_21", "I_22", "I_23", "I_24", "I_25", "I_26", "I_27", "I_28", "I_29", "I_30", "I_31", "I_32", "I_33", "I_34", "I_35", "I_36", "I_37", "I_38", 
            "I_39", "I_40", "I_41", "I_42", "I_43", "I_44", "I_45", "I_46", "I_47", "I_48", "I_49", "I_50", "I_51", "I_52", "II_01", "II_02", "II_03", "II_04", 
            "II_05", "II_06", "II_07", "II_08", "II_09", "II_10", "II_11", "II_12", "II_13", "II_14", "II_15", "II_16", "II_17", "II_18", "II_19", "II_20", "II_21", 
            "II_22", "II_23", "II_24", "II_25", "II_26", "II_27", "II_28", "II_29", "II_30","II_31", "II_32", "II_33", "II_34", "II_35", "II_36", "II_37", "II_38", 
            "II_39", "II_40", "II_41", "II_42","III_01", "III_02", "III_03", "III_04", "III_05", "III_06", "III_07", "III_08", "III_09", "III_10", "III_11", "III_12",
            "III_13", "III_14", "III_15", "III_16", "III_17", "III_18", "III_19", "III_20", "III_21", "TIPS_01", "TIPS_02", "TIPS_03", "TIPS_04" ]  

all_chapters_content = []

for chapter in chapters:
    # construct URL for each chapter
    chapter_url = f"{main_url}/{chapter}.html"
    print(f"Accessing {chapter_url}") 
    driver.get(chapter_url)

    # wait for page & MathJax to finish loading/rendering
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "div.main-content"))
        )
    except TimeoutException:
        print("Waiting a bit longer just in case...")
        time.sleep(5)

    # scrape content in order
    content_elements = []
    elements = driver.find_elements(By.CSS_SELECTOR, 'div.para, img, span.math, span.MathJax' )

    for i, element in enumerate(elements):
        if element.tag_name == 'div' and 'para' in element.get_attribute('class'):
            # scrape text from para
            text = re.sub(r'\s+', '', element.text).strip()
            content_elements.append({'type': 'text', 'data': text})

        elif element.tag_name == 'img':
            # download and save images
            img_src = element.get_attribute('src')
            if img_src and img_src.startswith('http'):
                content_elements.append({'type': 'img', 'data': img_src})
            elif img_src:
                img_url = main_url + img_src
                content_elements.append({'type': 'img', 'data': img_url})

        elif 'math' in element.get_attribute('class') or 'MathJax' in element.get_attribute('class'):
            # extract MathJax content
            math_text = element.get_attribute('data-latex') or element.text
            content_elements.append({'type': 'math', 'data': math_text})

    
    # structure chapters
    formatted_chapter_data = {
        'input': chapter,
        'output': content_elements
    }
    all_chapters_content.append(formatted_chapter_data)

    # close chromium
    driver.quit()

    # save data
    with open ('feynman_lectures_data.json', 'w') as f:
        json.dump(all_chapters_content, f, indent=4)
