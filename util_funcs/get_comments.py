from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

#Authenticate with your youtube api key
api_key = os.getenv("API_KEY")
youtube = build("youtube", "v3", developerKey=api_key)


#Fuction to fetch comments from youtube video
def get_comments(video_id):
  comments = []
  authors = []
  author_urls = []
  likes = []
  publishes = []
  updates = []

  request = youtube.commentThreads().list(
      part = "snippet",
      videoId = video_id,
      textFormat = "plainText"
  )
  while request:
    response = request.execute()
    for item in response["items"]:
      comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]

      comments.append(comment)

      request = youtube.commentThreads().list_next(request, response)

      #Creating a dataframe from scraped data
    comments_analytics = pd.DataFrame({"Comments":comments})
    comments_analytics.to_csv('util_funcs/comments.csv', index=False)


  return 'fetched comments'