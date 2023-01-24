# Sentiment Analysis

This repository contains code for a sentiment analysis of title on the New York Times Bestseller List. The analysis is carried out twice - once in R, and once in Python, and the documents are rendered using Quarto.

## Deploying Quarto to GitHub Pages

This repository also serves as a tutorial for publishing a Quarto document to GitHub pages. There are different ways to publish to GitHub Pages - see [quarto.org/docs/publishing/github-pages.html](https://quarto.org/docs/publishing/github-pages.html) for more information. 

To deploy from the command line, type:

```
quarto publish gh-pages sentiment_analysis.qmd
```

Here, I've specified the .qmd file since we're only publishing a single Quarto document rather than a website or book project. Otherwise, I get an error like:

```
ERROR: The specified path (G:\My Drive\GitHub\sentiment_analysis) is not a website or book project so cannot be published.
```