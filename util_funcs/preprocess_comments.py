# NLP libraries
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Text Preprocessing Libraries
import contractions
import re
# !pip install textacy
from textacy import preprocessing
import emoji


#Function to preprocess Comments to visualize them in word cloud
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
def preprocess_comments(text):
  text = contractions.fix(text)
  text = re.sub("http\S+", "", text)
  text = re.sub("\n", "", text)
  text = preprocessing.normalize.unicode(text)
  text = preprocessing.normalize.hyphenated_words(text)
  text = preprocessing.normalize.quotation_marks(text)
  text = preprocessing.normalize.whitespace(text)
  text = preprocessing.remove.accents(text)
  text = preprocessing.remove.brackets(text)
  text = preprocessing.remove.html_tags(text)
  text = preprocessing.remove.punctuation(text)
  text = preprocessing.replace.currency_symbols(text, "")
  text = preprocessing.replace.emails(text, "")
  text = preprocessing.replace.emojis(text, "")
  text = preprocessing.replace.hashtags(text, "")
  text = preprocessing.replace.numbers(text, "")
  text = preprocessing.replace.phone_numbers(text, "")
  text = preprocessing.replace.urls(text, "")
  text = preprocessing.replace.user_handles(text, "")
  text = emoji.replace_emoji(text, replace="")

  text = text.lower()
  words = word_tokenize(text)
  words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
  return words