from dotenv import find_dotenv, load_dotenv
from transformers import pipeline

load_dotenv(find_dotenv())

def llemma_test():
    pipe = pipeline("text-generation", model="EleutherAI/llemma_7b")

   # text = "Hello, I'm a language model"
   # print(pipe(text))

llemma_test()
