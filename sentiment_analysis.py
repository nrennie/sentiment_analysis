# read data
import pandas as pd 
nyt_titles = pd.read_csv("../nyt_titles.tsv", sep="\t") 

# select 1000 most popular and extract titles
text_data = nyt_titles.nlargest(n=1000, columns=['total_weeks'])
text_data = text_data[["title"]]

# split titles into words and make each a new row
text_data["title"] = text_data["title"].str.split() 
text_data = text_data.explode("title")

# change to lower case and remove commas
text_data["title"] = text_data["title"].str.lower()
text_data = text_data["title"].str.extractall(r"\s*([a-z@\d]+)[:\s]*")
text_data = text_data.droplevel(-1)
text_data = text_data.rename(columns={0: "word"})
text_data = text_data.reset_index()

# import afinn data
from afinn import Afinn
afn = Afinn(language = "en")

# remove stopwords
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
stopwords = set(STOPWORDS)
text_data = text_data[~text_data.word.isin(stopwords)]

# all words 
words = tuple(text_data.word.tolist())
scores = [afn.score(word) for word in words]

# convert to dataframe
sentiments = pd.DataFrame()
sentiments["word"] =  words
sentiments["scores"] = scores

# calculate average sentiment
import statistics as st
st.mean(sentiments["scores"]) # 0.02

# count number of each word
import numpy as np
counts = pd.value_counts(np.array(words))
plot_data = pd.DataFrame()
plot_data["word"] =  counts.index
plot_data["n"] =  counts.values

# filter < 3 ocurrences words
plot_data = plot_data.query('n >= 3')

# join data together
plot_data = plot_data.merge(sentiments, on="word", how="left")
plot_data = plot_data.drop_duplicates()

# word clouds
import matplotlib.pyplot as plt
text = " ".join(i for i in text_data.word)
wordcloud = WordCloud(stopwords=stopwords, 
                      background_color="white").generate(text)
plt.figure( figsize=(15,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
