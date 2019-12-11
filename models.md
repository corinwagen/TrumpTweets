---
title: Models 
layout: default
filename: models.md
--- 

##### Initial Model Architecture:

Attempts to fit simple tree-based models (e.g. Random Forest) to stock and bond data were ineffective. Therefore, we explored neural networks as an alternative approach to prediction. 

The models discussed below have been trained on individual or combinations of the predictors described in the "data" section, which include: 
- Tweet metadata
- Top mentioned users
- Word2vec embeddings
- Topic scores 
- Sentiment

Predictors were combined by day, and each day's data was supplemented with the previous n days' data, where d, the 'lookback', was a hyperparameter of the model. The resultant dataset was standardized and divided into a train dataset (first x days) and a test dataset (last 208 days). In order to mitigate some of the overfitting that might be caused by a small training dataset, we augmented the training datset through addition of noise to create a dataset k times larger than the original dataset (where k was 50, 100, or 500--see analysis section). 

Several different types of response data were modeled with these predictors: (1) Stock Market, (2) Bonds, (3) Gold, (4) Cryptocurrencies and Exchange Rates. These will each be addressed in turn. First, we will show the performance of each predictor dataset on each response set, and second in this and the analysis section on Chinese stocks and Gold, we will further investigate combinations of predictor sets in predicting these particular response variables.

The model architecture is a multi-layer neural network with l layers and n nodes per layer. To test each of the predictor sets individualy, an initial model was build with l=3 and n=32. After the initial models were trained, these hyperparameters were varied and performance was measured (see below)

##### Stocks:

###### American Stocks:

Individual predictor sets were fit on aggregated stock market data from the United States or from China. Performance on the American stocks, both classification and regression, was generally poor for all predictor sets.

![](assets/img/american_stocks1.single_predictor_set.regressor_pct_improvement.png')
![](assets/img/american_stocks1.single_predictor_set.classifier_auc.png')

###### Chinese Stocks:

However, performance on Chinese stocks was better, and depended on the predictor set. In general, for both classificaiton and for regression, the users either retweeted or mentioned in Trump's tweets were predictive of Chinese stock market volatility.

![](assets/img/chinese_stocks1.single_predictor_set.regressor_pct_improvement.png')
![](assets/img/chinese_stocks1.single_predictor_set.classifier_auc.png')

To validate the significance of this models, a top-performing model was refit 500 times and compared with *y*-randomized controls (Figure xx). 
The mean improvement over random was 18.6%, and the high *t*-statistic of -22.51 (*p* < 1e-90) demonstrates that the model performs significantly better than random. 

![](assets/img/china_ttest.png)

**Figure xx**: Frequent Handles Dataset Enables Modelling of Chinese Stock Volatility

###### Thirty-Year Treasury Bonds:

Modelling of bond volatility was found to be largely ineffective: although various outliers gave noticeable improvements over *y*-randomized models, 
the overall distribution of model performance implied that this was merely an artifact (Figure xx). 
Accordingly, these models were not investigated further.

![](assets/img/bond_predictors.png)

**Figure xx**: Effect of Different Predictor Sets on Modelling Bond Volatility

###### Gold Prices:

In contrast, modelling volatility in gold prices was more successful: in particular `word2vec`-based predictors sets gave marked improvement over *y*-randomized models (Figure xx). 
Raising dropout coefficients was found to be important to reduce the variance of the models (which is consistent with the pseudo-ensemble effect of neural networks with high dropout) (Figure xx).

![](assets/img/au_predictors.png)

**Figure xx**: Effect of Different Predictor Sets on Modelling Gold Volatility

![](assets/img/au_dropout.png)

**Figure xx**: Effect of Different Dropout Coefficients on Modelling Gold Volatility

To validate the significance of these models, a top-performing model employing `word2vec` predictors was refit 500 times and compared with *y*-randomized controls: 
the model consistently outcompeted the controls, as demonstrated by a *t*-statistic of -44.19 (*p* < 1e-200) (Figure xx).
The mean improvement was 7.3%, in line with the improvement seen earlier (*vide supra*).

![](assets/img/au_ttest.png)

**Figure xx**: `word2vec`-based Models Consistently Perform Better Than Chance

###### Cryptocurrencies and Exchange Rates:

Modeling volatility in cryptocurrencies and in foreign exchange rates (namely, the Canadian dollar (CAD) and the Russian ruble (RUB)), on single predictor sets that had performed well in the context of other responses (namely keyword embeddings, document embeddings, and handles of people mentioned in tweets), did not yield significant improvements over random (Figure XXX).

![](assets/img/currencies_exchange_1.percent_improvement.png)


########
An initial hit (for modelling combined American stock volatility) was found using a 3-layer dense neural network, 
with 32 `relu` nodes per layer and a single linear output node (using the `adam` optimizer in TensorFlow to optimize mean absolute error). 
A 30% dropout rate and hybrid L1/L2 regularization were found to attenuate overfitting to the training set; 
additionally, early stopping was found to be beneficial. 

Batch normalization was investigated but found to be ineffective. 

After 200 epochs of training, the neural network was found to consistently outperform a *y*-randomized control (by 7%).  

![](assets/img/initial_model_pred.png)

**Figure 1**: Initial Predictions for Test Set and Training Set

![](assets/img/initial_model_loss.png)

**Figure 2**: Model Performance By Epoch

Permutation importance analysis of the initial model (using `eli5`) revealed that the most important tweets were those referring to the Ukraine/impeachment scandal. 

![](assets/img/initial_model_importance.png){:height="350px"}

**Figure 3**: Most Important Predictors For Initial Model

##### Further Development:

To more systematically probe the importance of various features and hyperparameters, full factorial optimization in predictor and hyperparameter space was carried out using the Cannon cluster. 
A 3-level dense neural network with 32 `relu` nodes per layer (and a single linear output node) was optimized using the `adam` optimizer. 
Days of lookback (between 0 and 5), dropout coefficient (between 0 and 0.5), and predictor set were systematically varied and the improvement over the average of 100 *y*-randomized controls calculated.
50-fold augmentation using random noise was carried out in all cases. 

Models were fit on individual predictor sets, with dropout and predictor lookback as described in the following table. Two types of models were fit: a regression model, which attempted to estimate the amount of volatility, and a classification model whose goal it was to predict whether the response value would go up or down in a given day. 

| Augmentation n | % Improvement | Test Loss |
|----------------|---------------|-----------|
| 50             | 10.39         | 0.68      |
| 100            | 3.77          | 0.59      |  
| 500            | 8.73          | 0.55      |  


