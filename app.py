from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL
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
    # get title of video
    try:
      with YoutubeDL() as ydl:
        info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={id}", download=False)
        # Get the video title from the info dictionary
        video_title = info_dict.get('title', None)
    except:
      video_title = "Unknown Title"
    st.write(f"**\n Transcript for: {video_title} (https://www.youtube.com/watch?v={id})**")
    try:
      fetched_transcript = ytt_api.fetch(id)
      time.sleep(1.5)  # Delay between requests to avoid rate-limiting
      for snippet in fetched_transcript:
          st.write(snippet.text)
    except:
      st.write(f"Error with getTranscripts(). Transcript could not be extracted.\n")

if st.button("Get Transcripts") and channel_url:
  with st.spinner("Pulling transcripts..."):
    video_ids = getVideoIds(channel_url)
    if not video_ids:
            st.warning("No videos found or failed to retrieve playlist.")
    else:
      getTranscripts(video_ids)
  
