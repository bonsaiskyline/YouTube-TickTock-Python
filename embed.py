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
      # embedding_filename = embedding_name + ".csv"
      # df[embedding_name] = [embedding]
      df = df.append({'name': embedding_name, 'embedding': embedding}, ignore_index=True)
      # df.to_csv('embedding/' + embedding_filename, index=False)
      df.to_csv('embedding/embedding-append.csv', index=False)

#     with open("./embedding/{}.csv".format(name), 'w') as output:
#       print(name)
#       path = "./videos/" + filename
#       transcript = transcribe(path)
#       output.write(transcript.text)

# text =
# df = pd.read_csv('embedding/embedding.csv')
# df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(text, model='text-embedding-ada-002'))
# df.to_csv('output/embedded_1k_reviews.csv', index=False)