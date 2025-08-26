import pandas as pd
# Visualization Libraries
from wordcloud import WordCloud, ImageColorGenerator
# from PIL import Image
from matplotlib import pyplot as plt

from util_funcs.get_comments import get_comments
from util_funcs.preprocess_comments import preprocess_comments
from util_funcs.predict import emotion_detection


def generate_wordclouds(video_Id, progress_bar = None):
  get_comments(video_Id)

  comments_df = pd.read_csv('util_funcs/comments.csv')

  total = len(comments_df)

  emotions = comments_df["Comments"].apply(lambda x: emotion_detection(x, progress_bar, total))

  comments_df["Emotions"] = emotions

  comments_df.to_csv('util_funcs/comments.csv', index=False)

  comments = comments_df['Comments'].apply(preprocess_comments)

  preprocessed_comments = []
  for comment in comments:
    comment = " ".join(comment)
    preprocessed_comments.append(comment)

  comments_df["Preprocessed Comments"] = preprocessed_comments

  comments_emotions = comments_df[["Preprocessed Comments", "Emotions"]]

  emotion_group = comments_emotions.groupby("Emotions")

  emotes = set(comments_emotions["Emotions"])


  #Accessing different emotion groups, converting them to list, convertnig lists to sring data and creating W
  for e in emotes:
    list_emotes = emotion_group.get_group(e)["Preprocessed Comments"].tolist()
    comment_count = len(list_emotes)

    if not list_emotes:
      print(f"⚠️ Skipping {e}, no comments found.")
      continue

    emotes_data = "".join(list_emotes).strip()

    if not emotes_data:
      print(f"⚠️ Skipping '{e}', no valid words to generate wordcloud.")
      continue


    wordcloud = WordCloud(background_color = "black", width = 1000, height = 800, max_words = 100, colormap = "Reds").generate(emotes_data)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title(f"{e.capitalize()}     Comments: {comment_count}", fontsize = 20)

    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.savefig(f"wordclouds/{e}.png", dpi = 450)
    plt.close()