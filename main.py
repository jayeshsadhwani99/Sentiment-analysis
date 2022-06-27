import json
import sys
from api_communication import save_transcript
from yt_extractor import get_video_info, get_audio_url

def save_video_sentiments(url):
    video_info = get_video_info(url)
    url = get_audio_url(video_info)
    if url:
        title = video_info['title']
        title = title.strip().replace(" ", "_")
        title = "data/" + title
        save_transcript(url, title, sentiment_analysis=True)
        return title + "_sentiments.json"

def get_positivity_ratio(filename):
    with open("data/" + filename, "r") as f:
        data = json.load(f)
    
    positives = []
    negatives = []
    neutrals = []
    for result in data:
        text = result["text"]
        if result["sentiment"] == "POSITIVE":
            positives.append(text)
        elif result["sentiment"] == "NEGATIVE":
            negatives.append(text)
        else:
            neutrals.append(text)
        
    n_pos = len(positives)
    n_neg  = len(negatives)
    n_neut = len(neutrals)

    print("Number of positives:", n_pos)
    print("Number of negatives:", n_neg)
    print("Number of neutrals:", n_neut)

    # ignore neutrals here
    r = n_pos / (n_pos + n_neg)
    print(f"Positive ratio: {r:.3f}")

if __name__ == "__main__":
    video_url = sys.argv(1)
    filename = save_video_sentiments(video_url)
    get_positivity_ratio(filename)