import json
import os

def process_file(file_path):
    messages = []
    skip_intro = True  # Flag to skip the initial introductory part

    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                if isinstance(data, list):  # If the data is a list, iterate through each item
                    for item in data:
                        if skip_intro:
                            # Skip entries until we find the first "user" role
                            if item['role'] == 'user':
                                skip_intro = False
                                messages.append(item)
                        else:
                            messages.append(item)
                else:
                    if skip_intro:
                        # Skip entries until we find the first "user" role
                        if data['role'] == 'user':
                            skip_intro = False
                            messages.append(data)
                    else:
                        messages.append(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {file_path}: {e}")
                continue

    return {"messages": messages}

def process_all_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".jsonl"):
            file_path = os.path.join(input_folder, filename)
            formatted_data = process_file(file_path)

            output_file_path = os.path.join(output_folder, filename)
            with open(output_file_path, 'w') as output_file:
                output_file.write(json.dumps(formatted_data, indent=2) + '\n')

# Define your input and output folder paths
input_folder = '/System/Volumes/Data/Users/srivatsakrishnamurthy/Documents/dev/FeynmanLibrary/data/conversation_data'
output_folder = '/System/Volumes/Data/Users/srivatsakrishnamurthy/Documents/dev/FeynmanLibrary/data/formatted_conversation_data'

# Process all files in the input folder
process_all_files(input_folder, output_folder)

