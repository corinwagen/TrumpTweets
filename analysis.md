---
title: Models 
layout: default
filename: models.md
--- 

##### Models: 

Several top-performing models were selected for further analysis, in order to obtain insight into the underlying mechanism of prediction. 

Given the massive complexity of the global stock market, we feel that explaining 7% of market volatility alone is not trivial. However, it is only a start.

###### Stocks:

The top-performing model for predicting Chinese stocks used Trump's frequent Twitter mentions in combination with a 5-day lookback to lower the mean absolute error by approximately 18%
(relative to a *y*-randomized model). 
Using `eli5`'s predictor importance feature (which shuffles various predictors and observes the loss in efficacy), the most important predictors could be extracted (Figure xx).

![](assets/img/best_china_pred.png){:height="350px"}

**Figure xx**: Top Predictors of Chinese Stock Variance

Notably, two contributors to Fox News occupied the top positions (Mollie Hemingway and Maria Bartiromo), with other news sources (NBC, CNN, ABC) featuring prominently as well. 
It is plausible that Trump mentions these people disproportionately when significant news events are occuring (which will concomitantly impact the Chinese stock market),
but more research and experimentation is needed before conclusive results can be obtained. 

![](assets/img/maria_tweet.png){:width="500px"}

**Figure xx**: A sample tweet (@MariaBartiromo) which might impact Chinese stock volatility

###### Gold Prices:

###### Ruble Exchange Rate:

