import openai
import os
import pandas as pd

openai.api_key = os.environ['OPENAI_API_KEY']

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

df = pd.DataFrame()
for filename in os.listdir("./transcription"):
  if filename.endswith(".txt"):
    with open("./transcription/" + filename, 'r') as f:
      text = f.read()
      embedding = get_embedding(text, "text-embedding-ada-002")
      embedding_name = filename.replace(".txt", "")
      df = df.append({'name': embedding_name, 'embedding': embedding}, ignore_index=True)
      df.to_csv('embedding/embedding-append.csv', index=False)
