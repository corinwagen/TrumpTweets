---
title: Analysis 
layout: default
filename: analysis.md
--- 

#### Predictor Analysis:

Several top-performing models were selected for further analysis, in order to obtain insight into the underlying mechanism of prediction. 
Although the predictive power of these models is, in general, small, 
we feel that any ability to reproducibly explain the massive complexity of the global stock market is exciting and worthy of further study. 

###### Stocks:

The top-performing model for predicting Chinese stocks used Trump's frequent Twitter mentions in combination with a 5-day lookback to lower the mean absolute error by approximately 18%
(relative to a *y*-randomized model). 
Using `eli5`'s predictor importance feature (which shuffles various predictors and observes the loss in efficacy), the most important predictors could be extracted (Figure 1).

![](assets/img/best_china_pred.png){:height="350px"}

**Figure 1**: Top Predictors of Chinese Stock Variance

Notably, two contributors to Fox News occupied the top positions (Mollie Hemingway and Maria Bartiromo), with other news sources (NBC, CNN, ABC) featuring prominently as well. 
It is plausible that Trump mentions these people disproportionately when significant news events are occuring (which will concomitantly impact the Chinese stock market) (Figure 2),
but more research and experimentation is needed before conclusive results can be obtained. 

![](assets/img/maria_tweet.png){:width="500px"}

**Figure 2**: A sample tweet (@MariaBartiromo) which might impact Chinese stock volatility

###### Gold Prices:

As a safe alternative to stocks or bonds which holds its value even through total state collapse, the price of gold historically tracks with economic uncertainty. 
The top-performing model for predicting gold prices was based on topic analysis done by `word2vec` (as described previously), which permitted facile extraction of the most important topics 
(Figure 3).

![](assets/img/au_importance.png){:height="350px"}

**Figure 3**: Top Predictors of Gold Price Variance

Several `word2vec` topics were especially important in describing volatility in gold prices: tweets about China or Beijing, and tweets about Dakota. 
The first category presumably reflects the effect of the trade war on the US economy,
whereas the second likely refers to the booming oil industry of North Dakota (and the oil pipelines built there). 
Both of these topics would be expected to impact economic uncertainty significantly, and thus this model seems physically reasonable (Figure 4). 

![](assets/img/dakota_tweet.png){:width="500px"}

**Figure 4**: A sample tweet about North Dakota which might affect the economy

###### Ruble Exchange Rate:

The top-performing model for predicting volatility in the ruble exchange rate also used `word2vec` predictors. 
In contrast to the gold model, there were no "standout" predictors for the ruble variance model: 
instead, many predictors assumed roles of lesser importance. 
Foreign policy appeared to be a commonality, with tweets pertaining to South Korea, the Kurds, Yemen, Lebanon, and China seeming to have the biggest impact (Figure 5).

The considerable global influence wielded by Trump (and Russia) means that any bold foreign policy claims are likely to affect the Russian government, and thereby the Russian currency.
Accordingly, these predictors seem reasonable for describing volatility in the ruble/dollar exchange rate. 

![](assets/img/ruble_importance.png){:height="350px"}

**Figure 5**: Top Predictors of Ruble/Dollar Exchange Rate Variance

##### Conclusions:

The original goal of this project was to examine how Donald Trump's tweets impacted market confidence, both domestically and in international markets. 
These results indicate that a small but non-zero amount of market variance across diverse indices can be explained by Trump's tweets, 
particularly those pertaining to American foreign policy. 

It is fundamentally difficult to deconvolute the impact of Trump's *tweets* and the impact of Trump's *actions*: 
certainly, initiating a trade war with China would affect market indices regardless of tweets (or lack thereof). 
Since this is the real world, we cannot perform an A/B test in which we examine the effect of only Trump's tweets; 
it is likely that the observed correlation does not directly translate to causation (at least, not to the degree our models imply). 
Nevertheless, it is remarkable and surprising that so simple a predictor as Trump's tweets are able to describe a substantial amount of the chaos of global markets.

These data are extremely preliminary, and our conclusions could be greatly strengthened in many ways.
We have summarized [a number of our ideas for further research](future_work.html), and hope that this analysis might serve as a stepping-stone for further insights in this area. 
