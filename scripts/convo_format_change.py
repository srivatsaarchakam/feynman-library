import os
import json

def convert_format(data):
    messages = []
    for entry in data:
        if entry.get("role") == "user" or entry.get("role") == "assistant":
            messages.append({
                "role": entry["role"],
                "content": entry["content"]
            })
    return {"messages": messages}

def process_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    
    files = os.listdir(input_folder)
    if not files:
        print(f"No files found in the input folder: {input_folder}")
        return

    for filename in files:
        if filename.endswith(".json") or filename.endswith(".jsonl"):
            file_path = os.path.join(input_folder, filename)
            print(f"Processing file: {file_path}")
            try:
                data = []
                with open(file_path, 'r') as file:
                    if filename.endswith(".jsonl"):
                        for line in file:
                            data.append(json.loads(line))
                    else:
                        data = json.load(file)
                    
                    print(f"Loaded data from {file_path}")
                    for item in data:
                        print(item)  # Debug: Print each item in the data list

                    converted_data = convert_format(data)
                    print(f"Converted data: {converted_data}")
                    
                    output_filename = filename.rsplit('.', 1)[0] + '.jsonl'
                    output_path = os.path.join(output_folder, output_filename)
                    with open(output_path, 'w') as outfile:
                        for item in converted_data['messages']:
                            json.dump(item, outfile)
                            outfile.write('\n')
                    print(f"Saved converted data to: {output_path}")
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")
        else:
            print(f"Skipping non-JSON file: {filename}")

input_folder = '/System/Volumes/Data/Users/srivatsakrishnamurthy/Documents/dev/FeynmanLibrary/data/conversation_data'
output_folder = '/System/Volumes/Data/Users/srivatsakrishnamurthy/Documents/dev/FeynmanLibrary/data/formatted_conversation_data'

# Ensure the input folder exists
if not os.path.exists(input_folder):
    print(f"Input folder does not exist: {input_folder}")
else:
    # Process the files
    process_files(input_folder, output_folder)
