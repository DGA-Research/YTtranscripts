from youtube_transcript_api import YouTubeTranscriptApi
import subprocess
import time
import streamlit as st

st.set_page_config(page_title="YouTube Channel Transcripts", layout="wide")
st.title("YouTube Channel Transcripts")

channel_url = st.text_input("Enter YouTube Channel URL (e.g. https://www.youtube.com/@andybiggs2257):")

# function to pull a list of video ids for a youtube channel
def getVideoIds(url):
  command = f"yt-dlp --flat-playlist --print id {url}"
  try:
      output_bytes = subprocess.check_output(command, shell=True)
      command_output = output_bytes.decode('utf-8')  # Decode to string

      # Split output into a list of lines (video IDs)
      video_ids = command_output.strip().split('\n')

      return(video_ids)

  except subprocess.CalledProcessError as e:
      print(f"Error executing command: {e}")

# function to get transcripts for each of these ids
def getTranscripts(video_ids):
  ytt_api = YouTubeTranscriptApi()
  for id in video_ids:
    print(f"\n Transcript for: https://www.youtube.com/watch?v={id}")
    try:
      fetched_transcript = ytt_api.fetch(id)
      time.sleep(1.5)  # Delay between requests to avoid rate-limiting
      for snippet in fetched_transcript:
          print(snippet.text)
    except:
      print(f"Error with getTranscripts(). Transcript could not be extracted for https://www.youtube.com/watch?v={id}\n")

if st.button("Get Transcripts") and channel_url:
  with st.spinner("Pulling transcripts...")
    video_ids = getVideoIds(channel_url)
    if not video_ids:
            st.warning("No videos found or failed to retrieve playlist.")
else:
  getTranscripts(video_ids)
  
