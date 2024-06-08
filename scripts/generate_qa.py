import json
import spacy
from transformers import pipeline

# load NLP Model and the question generation pipline
nlp = spacy.load("en_core_web_sm")
q_generator = pipeline("text2text-generation", model="valhalla/t5-small-qg-prepend")

def generate_convo(text):
    doc = nlp(text)
    messages = []
    for sent in doc.sents:
        generated = q_generator("generate question: " + sent.text, max_length=512)
        question  = generated[0]['generated_text']
        for item in generated:
            messages.append({"role": "user", "content": question})
            messages.append({"role": "assistant", "content": sent.text})

    return {"messages":messages}

def process_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        all_conversations = []

        for entry in data:
            text_entries = [item['data'] for item in entry['output'] if item['type'] == 'text'][:10]
            text = " ".join(text_entries)
            conversation = generate_convo(text)
            all_conversations.append(conversation)

    return all_conversations

# current data path
file_path = file_path = '/Users/srivatsakrishnamurthy/Documents/dev/FeynmanLibrary/data/feynman_lectures_data.json'
conversations = process_data(file_path)

# save new data
with open('/data/formatted_data.json', 'w') as f:
    json.dump(conversations, f, indent=4)
