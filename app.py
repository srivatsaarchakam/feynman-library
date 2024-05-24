from dotenv import find_dotenv, load_dotenv
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

load_dotenv(find_dotenv())

def llemma_test():

    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/llemma_7b")  # Set legacy to False if you understand the implications
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/llemma_7b")

    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=100)  # Control the generation length more precisely

    text = "I have a math problem that I need help with: Solve the equation 2x + 3 = 11 for x."
    print(pipe(text))

llemma_test()