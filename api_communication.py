from textwrap import indent
import time
import requests
import json
from api_secrets import API_KEY_ASSEMBLYAI

# Step 1
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcription_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {'authorization': API_KEY_ASSEMBLYAI, "content-type": "application/json"}

CHUNK_SIZE = 5242880  # 5MB

def upload(filename):
    def read_file(filename, chunk_size=CHUNK_SIZE):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data
    response = requests.post(upload_endpoint,
                            headers=headers,
                            data=read_file(filename))

    audio_url = response.json()['upload_url']
    return audio_url

# Step 2
def transcribe(audio_url, sentiment_analysis):
    json = { "audio_url": audio_url, 'sentiment_analysis': sentiment_analysis }
    response = requests.post(transcription_endpoint, json=json, headers=headers)
    job_id = response.json()['id']
    return job_id

# Step 3
def poll(job_id):
    polling_endpoint = transcription_endpoint + "/" + job_id
    response = requests.get(polling_endpoint, headers=headers)
    return response.json()

def transcription_result_url(audio_url, sentiment_analysis):
    job_id = transcribe(audio_url, sentiment_analysis)
    while True:
        response = poll(job_id)
        if response['status'] == 'completed':
            return response, None
        elif response['status'] == 'error':
            return response, response["error"]

        print("Waiting 30 seconds for transcription to finish...")
        time.sleep(30)

# Step 4
def save_transcript(audio_url, filename, sentiment_analysis=False):
    data, error = transcription_result_url(audio_url, sentiment_analysis)
    if data:
        text_filename = filename + ".txt"
        with open(text_filename, 'w') as f:
            f.write(data['text'])

        if sentiment_analysis:
            sentiment_filename = filename + ".json"
            with open(sentiment_filename, 'w') as f:
                sentiments = data['sentiment_analysis_results']
                json.dump(sentiments, f, indent=4)
        print("Transcription saved to " + text_filename)
    elif error:
        print("Error: " + error)