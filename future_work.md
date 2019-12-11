---
title: Future Work 
layout: default
filename: future_work.md
--- 

#### Future Work:

Although the initial results are promising, there is much that could be done to improve the quality of these data and strengthen the conclusions. 

##### Improved Data: 

Better and more random stock selection:
 - taking an average of more stocks (both a simple random sample and those which we picked which were particularly vulnerable to the trade war. We could also weight stocks by how much total money is being traded per stock, and make our weighted average thus.

###### Better Data Augmentation:

As mentioned previously ([*vide supra*](models.md)), applying purely numerical data augmentation to the final predictor set had

###### More Sophisticated Sentiment Analysis:

###### 

###### Response Variables:

Stocks:
To calculate volatility in a more complex way we could consider 

The two easiest things we could do to improve our response variable are:

Moving Averages
 - We could take moving averages. However, given that Trump tweets so often, and many times a day, our prior belief was that his tweets would affect intraday prices Or just a bit into the future. That is, our model's response variable implicitly assumes a short memory for tweets. We could easily expand this into moving averages. But how long would those moving averages be? How would we select the length? This adds a degree of complexity into making the response variable that gets away from the raw data, which is why we didn't go that route.
 
 ![](stocks/moving_avg_plots/AAPL_movavg.png)
 
 
 ![](stocks/moving_avg_plots/CORN_movavg.png)
 
 ![](stocks/moving_avg_plots/BABA_movavg.png)
  
 ![](stocks/moving_avg_plots/DJI_movavg.png)
 


 
 Volume information and Momentum
 - Including the volume coefficient in some way. We could add the volume term to our model's calculations, but given our log-normal assumptions and justifications for our response transformations, we would probably need to meet with teaching staff to discuss how to do this. Specifically, we did meet with Kevin Rader on Thursday december 5th, and he suggested a simple interday difference to get normal looking histograms for our response variable.
 - If given more time, we would like to add momentum term to the model, say to the coffefficient of volume as before. However, we can think of two associated hyper-parameters which would be associated with such a term: the power to which it would be raised as well as a llambda (from regularization) analygous parameter we would need to tune.

Multiple Stock Response Variables
 - we could better split the response variables and consider response variable splits for example:
    - we could split stocks up by industry. For example, we could consider only farm stocks or only superconductor stocks.
    - we could split up stocks by country. The issue here is time difference. We only had inter-day data. Therefore if Trump tweets something about the trade war today, on 12/10, then it could be read as changing China's stock price on 12/11. This complicated our model in a such a way that we chose not to approach these more complicated country splits. Also, multiple response variables may have complex joint distributions which, given our collective backgrounds in CS 209a and stat 139 at Harvard, we don't necissarilly have to background to address.

##### More Sophisticated Models
