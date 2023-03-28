import openai
import os
import pandas as pd

openai.api_key = os.environ['OPENAI_API_KEY']

def get_embedding(
  text,
  model="text-embedding-ada-002"
  ):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

dfs = []
for filename in os.listdir("./transcription"):
  if filename.endswith(".txt"):
    path = "./transcription/" + filename
    video_name = filename.replace(".txt", "")
    with open(path, 'r') as f:
      text = f.read()
      embedding = get_embedding(text, "text-embedding-ada-002")
      dfs.append(pd.DataFrame([[video_name, embedding]], columns=['video_name', 'embedding']))
result_df = pd.concat(dfs, axis=0)
result_df.to_csv('embedding/embedding.csv', index=False)
