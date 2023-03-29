
import boto3
import json
session = boto3.Session(profile_name='eb-cli')
s3 = session.client('s3')

bucket_name = 'yt-tiktok'
key_name = 'ouput.json'

response = s3.get_object(Bucket=bucket_name, Key=key_name)
text = response['Body'].read().decode('utf-8')
data = json.loads(text)
items = data['results']['items']
for item in items:
    print(item['alternatives'][0]['content'] + ' ' + item['speaker_label'])