import json
import os

data_directory = '/System/Volumes/Data/Users/srivatsakrishnamurthy/Documents/dev/FeynmanLibrary/data'
os.makedirs(data_directory, exist_ok=True)


# Load your JSON data
with open('data/feynman_lectures_data.json', 'r') as file:
    data = json.load(file)

# Modify the data by removing the first 14 items from each 'output' section starting from "I_07"
for item in data:
    if item['input'] >= 'I_07':  
        if len(item['output']) > 14:  
            item['output'] = item['output'][14:]  


json_filename = os.path.join(data_directory, 'feynman_lectures_data.json')

# Save the modified data back to a new JSON file
with open(json_filename, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)

print("First 14 outputs removed from sections starting from I_07 onward.")


