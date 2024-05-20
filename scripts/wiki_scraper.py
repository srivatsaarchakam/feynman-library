import requests
from bs4 import BeautifulSoup
import json
from sklearn.model_selection import train_test_split

url = "https://en.wikipedia.org/wiki/Richard_Feynman"

response = requests.get(url)

if response.status_code == 200:
    print("Page Fetched Successfully!")

    # parse the content with Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # The titles in the wiki article to exclude
    exclude_titles = ['Bibliography', 'References', 'Sources', 'Further reading', 'External links']

    # collect the headers except the excluded ones
    data = []
    for header in soup.find_all(['h2', 'h3', 'h4','h5', 'h6']):
        # check if header is an excluded one
        if header.get_text(strip = True).split('[')[0].strip() not in exclude_titles:
            # extract all text from the next paragraphs
            content = []
            for sibling in header.find_next_siblings(['p', 'h2', 'h3', 'h4', 'h5', 'h6']):
                if sibling.name == 'p':
                    content.append(sibling.get_text(strip = True))
                else:
                    break

            section_text = ' ' .join(content)
            data.append({'input': header.get_text(' ', strip = True).split('[')[0].strip(), 'output': section_text})


    # saving data to json files
    with open('wiki_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

else:
    print("Failed to fecth the page. Status code:", response.status_code)