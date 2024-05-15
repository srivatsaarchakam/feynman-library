from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from sklearn.model_selection import train_test_split
import json
import re

# chrome webdriver setup
service = Service('/System/Volumes/Data/Users/srivatsakrishnamurthy/Documents/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)

# main url where all of the content is coming from
main_url = "https://www.feynmanlectures.caltech.edu"

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
    print(f"Accessing {chapter_url}")  # Debug: print the URL being accessed

    # use webdriver to navigate to the constructed url
    driver.get(chapter_url)
    
    # scrape chapter content
    paragraphs = driver.find_elements(By.CSS_SELECTOR, 'div.para')

    # join all paragraphs into one single one
    chapter_text = ' '.join(para.text for para in paragraphs)

    # replace multiple blank spaces with one
    chapter_text = re.sub(r'\s+', ' ', chapter_text).strip()  

    # chapter data formated into "input:" & "output:"
    formatted_chapter_data = {
        'input': chapter,
        'output': chapter_text
    }

    all_chapters_content.append(formatted_chapter_data)

# close browser after scraping
driver.quit()

# data split for training and testing
train_data, test_data = train_test_split(all_chapters_content, test_size=0.2, random_state=42)

# save training in training file
with open('feynman_lectures_training_data.json', 'w') as f:
    json.dump(train_data, f, indent=4)

# save testing in testing file
with open('feynman_lecture_testing_data.json', 'w') as f:
    json.dump(test_data, f, indent=4)

