library(dplyr)
library(readr)
library(tidytext)
library(ggplot2)
library(ggwordcloud)

# Data --------------------------------------------------------------------

# read in data
nyt_titles <- read_tsv("../nyt_titles.tsv")

# select 1000 most popular books and extract titles
text_data <- nyt_titles %>% 
  slice_max(total_weeks, n = 1000, with_ties = FALSE) %>% 
  select(title)


# Sentiment analysis ------------------------------------------------------

# load stop words and sentiments data sets
data(stop_words)
afinn_df <- get_sentiments("afinn")

# prep text data and remove stop words
text_data <- text_data %>% 
  unnest_tokens(word, title) %>% 
  anti_join(stop_words, by = "word")

# join sentiments data to titles
sentiments <- text_data %>% 
  inner_join(afinn_df, by = "word") 

# calculate mean sentiment
sentiments %>% 
  pull(value) %>% 
  mean()


# Word clouds -------------------------------------------------------------

# calculate number of occurrences of each word
counts <- text_data %>% 
  group_by(word) %>%  
  mutate(count = n())

# join counts data and sentiments data
plot_data <- counts %>% 
  left_join(sentiments, by = "word") %>% 
  distinct()

# remove any words with less than three occurrences
plot_data <- plot_data %>% 
  filter(count > 2) %>% 
  arrange(desc(count))

# create word cloud
set.seed(42)
set.seed(42)
ggplot(data = plot_data, 
       mapping = aes(label = word, size = count, colour = value)) +
  geom_text_wordcloud() +
  scale_size_area(max_size = 15) +
  scale_colour_gradient2(low = "#710193", 
                         high = "#2e6930", 
                         na.value = "#dedede", 
                         limits = c(-5, 5)) +
  theme_void()






