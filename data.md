---
title: Data 
layout: default
filename: data.md
--- 

### Data:
 
 - [Tweets](#tweets)
 - [Stocks](#stocks)
 - [Bonds](#bonds)
 - [Other](#other)

### Tweets: 

Tweets were downloaded from the [Trump Twitter Archive](http://www.trumptwitterarchive.com/archive) and analyzed using the Jupyter notebook `tweets/parse_tweets.ipynb`. 
Only tweets between January 20th, 2017 and October 30th, 2019 were selected, which led to 11,717 entries. 

#### Simple Tweet Predictors:

Most metadata were collected automatically through the Trump Twitter Archive, but some (`num_mentions`, `num_retweets`) had to be collected in Python. 
The tweet text was then sanitized for downstream analysis by removing Twitter-specific marks (e.g. “@”, “#” to denote mentions and hashtags, respectively) and HTML entities (`&amp;`). 
The tweets were then split into words using the Python library `nltk` (using a pretrained model), and parts of speech were assigned.

![](assets/img/image6.png)

**Figure 1**: Histograms of tweet metadata and selected descriptors.

Initial topic analysis was done using human-defined lists of keywords: for instance, a tweet containing the word “Moscow”, “Putin”, or “Russian” would be flagged as `keyword_Russia`. 
Using this method, we found that approximately 70% of tweets could be assigned with at least one keyword (Figures 1, 2). 
This strategy, although crude, allowed us to develop baseline models to compare against more refined predictor sets, 
and also serves as a useful reality check to use in combination with automated topic extraction. 
The current keywords show a relatively small degree of multicollinearity, which indicates that the user-defined topics can serve as a passable predictor set (Figure 3).

![](assets/img/image4.png){:height="450px"}

**Figure 2**: Manually assigned keywords, summed by day. 

![](assets/img/image1.png)

**Figure 3**: Correlation matrix for keyword and metadata predictors.

#### Natural Language Modelling of Tweets:

As Twitter text is informal and limited in the number of characters, it lends itself to usage of many, and likely rapidly changing, abbreviations and societal references. 
Many such abbreviations, if we can pick them out, could be quite useful in building a keyword search. 
However, this also means that the number of keywords for a particular topic could potentially become arbitrarily large and hard to cull by hand. 
This motivates the use of two different types of models: 
(1) topic models, which aim to find groups of words that form recurring ‘topics’ in the particular set of tweets, as well as 
(2) word embeddings, which assume that high-dimensional word space can be projected onto a lower-dimensional manifold, such that related words lie close to one another in lower-dimensional space.

##### Word Embeddings:

As previously discussed, using keywords informed by domain knowledge will likely be helpful for our prediction task; 
however, it might not be feasible to come up with an exhaustive list of all keywords that might be used in any text. 
Therefore, we are investigating the use of word embeddings (*vide supra*). 
In particular, we are using Google’s pre-trained `word2vec` skipgram embedding, which transforms each word into a vector of length 300.

Our first investigations involved comparing the `word2vec` embedding with the previously established keywords. 
Every valid word in the Trump tweets was compared to every aforementioned keyword using cosine similarity; 
the top 10 most similar words in the tweets for some exemplar keywords are shown in Figure 4. 
Using this metric, we can now take advantage of a larger breadth of vocabulary, while still using our domain knowledge. 
Notably, only a small proportion of tweet word space has a cosine similarity of  >0.5 (Figure 5), which suggests that this method might not trade sensitivity for significant reductions in specificity.
Admittedly, this particular embedding, while extensive, was produced in 2013; certain contemporary political figures, events, and other references might not be appropriately represented in this model.
Additionally, social media-specific terms including hashtags and emojis will not be captured by the pre-trained embeddings. 
Looking forward, we will likely augment the word embeddings with rationally chosen subsets of keywords that do not appear in the pretrained `word2vec` model; 
with more time, it might be advantageous to train a skipgram on a large corpus of tweets and use updated embeddings.

![](assets/img/image3.png)

**Figure 4**: Top 10 keyword associations with words found in tweets based on embeddings from `word2vec` skipgram model.

![](assets/img/image7.png)

**Figure 5**: Distribution of cosine similarities between each keywords and each word in tweets (left) and proportion of tweets with cosine similarity between a keyword and a word in the tweet such that the similarity is above a particular threshold (i.e., the tweet is “activated” by at least one keyword) (right).

