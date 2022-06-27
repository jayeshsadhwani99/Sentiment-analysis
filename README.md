# Sentiment Analysis

This project uses Assembly AI API to analyse a youtube video
and prints the positivity ratio

# How to use

1. Install packages

   `pip install -r requirements.txt`

2. Get a youtube video

3. Run the program

   `python main.py video_url`

# How does it work?

1. Firstly, we get the data from youtube, like the title and the audio,
   using the `youtube-dl` package

2. We send it to assembly ai to transcript the file and perform sentiment
   analysis

3. We analyse the result and calculate the positivity ratio
