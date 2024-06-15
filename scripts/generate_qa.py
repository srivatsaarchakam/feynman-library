import json
import spacy
from transformers import pipeline
from huggingface_hub import notebook_login

# load question generation pipline
nlp = spacy.load("en_core_web_sm")
q_generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.3")

def clean_text(text):
    return text.encode('ascii', 'ignore').decode('ascii')

def generate_convo(text, excerpt_number):
    """Generate conversation for a given cleaned text, including prompt handling."""
    cleaned_text = clean_text(text)
    if not cleaned_text.strip():
        return [{"role": "user", "content": f"No input text provided after cleaning for excerpt {excerpt_number}."}]

    print(f"Processing excerpt number: {excerpt_number}")

    prompt_text = f"""
    Given the following excerpt from Richard Feynman's lectures: '{cleaned_text}'
    Imagine you are a student seeking to understand physics concepts discussed here.
    Please generate five questions a student might ask based on the excerpt and provide answers as if you are Richard Feynman explaining the concepts or related physics phenomena.
    """
    generated = q_generator(prompt_text, max_new_tokens=500, num_return_sequences=1)
    response = generated[0]['generated_text']

    # Process the generated output into structured Q&A pairs
    messages = []
    q_and_a_list = response.split("\n")  # Split by new lines as a basic way to possibly separate questions and answers

    for line in q_and_a_list:
        if line.strip():
            # Remove unwanted prefixes and numbering from questions and answers
            line = line.replace("1. Question:", "").replace("2. Question:", "").replace("3. Question:", "").replace("4. Question:", "").replace("5. Question:", "").strip()
            line = line.replace("Answer:", "").strip()

            # Separate questions and answers based on context or format clues
            if line.endswith('?'):
                messages.append({"role": "user", "content": line})
            else:
                messages.append({"role": "assistant", "content": line})

    return messages

def process_data(file_path, output_file_path):
    """Process each text excerpt individually from the JSON file and save to a .jsonl file."""
    with open(file_path, 'r') as file, open(output_file_path, 'w') as outfile:
        data = json.load(file)
        excerpt_number = 1  # Start numbering from 1

        for entry in data:
            for item in entry['output']:
                if item['type'] == 'text':
                    text = item['data']
                    conversation = generate_convo(text, excerpt_number)
                    json.dump(conversation, outfile)
                    outfile.write('\n')  # Ensure each conversation is on a new line
                    excerpt_number += 1

# sample test on excerpt #1 so that we can see if the processing & q/a generation works
# first_text = "This two-year course in physics is presented from the point of view that you, the reader, are going to be a physicist. This is not necessarily the case of course, but that is what every professor in every subject assumes! If you are going to be a physicist, you will have a lot to study: two hundred years of the most rapidly developing field of knowledge that there is. So much knowledge, in fact, that you might think that you cannot learn all of it in four years, and truly you cannot; you will have to go to graduate school too!"
# first_excerpt_number = 1
# result = generate_convo(first_text, first_excerpt_number)
# print(result)

# current data path
input_file_path = 'batched_lecture_data.json'
output_file_path = 'processed_conversations.jsonl'
process_data(input_file_path, output_file_path)
print('Completed Processing')