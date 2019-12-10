---
title: Models 
layout: default
filename: models.md
--- 

#### Models: 

##### Model Architecture:

Attempts to fit simple tree-based models (e.g. Random Forest) to stock and bond data were almost totally ineffective. 

The following datasets were combined to form a hybrid predictor set: 
- Tweet metadata
- Top mentioned users
- Word2vec embeddings
- Topic scores 
- Sentiment

Predictors were combined by day, and each day's data was supplemented with the previous 10 days' data. 
The resultant dataset (692 rows) was standardized and divided into a train dataset (first 595 rows) and a test dataset (last 86 rows, chronologically).
The train dataset was augmented through addition of random noise. 

An initial hit (for modelling combined American stock volatility) was found using a 3-layer dense neural network, 
with 64 `relu` nodes per layer and a single linear output node (using the `adam` optimizer in TensorFlow to optimize mean absolute error). 
A 30% dropout rate and hybrid L1/L2 regularization were found to attenuate overfitting to the training set; 
additionally, early stopping was found to be beneficial. 

After 200 epochs of training, the neural network 

![]('assets/img/initial_model_pred.png')

**Figure 1**: Initial Predictions for Test Set and Training Set

![]('assets/img/initial_model_loss.png')

**Figure 2**: Model Performance By Epoch
