import json
import spacy
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# load spacy & mistral-7b-instruct
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
mistral_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

# q/a pairs generation & propmpting
def generate_qa_pairs(text):
    prompt = f"Input Text: {text}\n"\
             "Context:Answering Physics Questions Based on Richard Feynman's Lectures on Physics\n" \
             "Given the text excerpt provided, create five standalone question and answer pairs where each question contains a question about physics or about the life of Richard Feynman. The questions should explore the underlying physics concepts, Feynman's interpretations as presented in the text, or information about his life. Answers should directly use, verbatim, phrases or sentences from the text to ensure accuracy and maintain the original context of Feynman's teachings. Each question and answer pair should be crafted as if they are independent, without requiring context from other pairs, and should vary in style to cover different aspects or perspectives of the content. Do not number the questions."
    
    generated = mistral_generator(prompt, max_new_tokens=250)[0]['generated_text']
    return generated

# data processing
def process_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        all_conversations = []

        for entry in data:
            text_entries = [item['data'] for item in entry['output'] if item['type'] == 'text'][:1]
            text = " ".join(text_entries)
            generated_qa_pairs = generate_qa_pairs(text)
            all_conversations.append({"messages": generated_qa_pairs})

    return all_conversations

conversations = process_data("/Users/srivatsakrishnamurthy/Documents/dev/FeynmanLibrary/data/feynman_lectures_data.json")

save_path = "/Users/srivatsakrishnamurthy/Documents/dev/FeynmanLibrary/data/qa_pairs.jsonl"
with open(save_path, 'w') as f:
    json.dump(conversations,f, indent=4)
