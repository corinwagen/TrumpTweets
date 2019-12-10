#!/usr/bin/python
import argparse
import copy
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import scipy as sp
import tensorflow as tf

from functools import reduce
from sklearn.metrics import auc
from sklearn.metrics import roc_curve
from sklearn.preprocessing import MinMaxScaler

parser = argparse.ArgumentParser()

## input data arguments
parser.add_argument('--config', type=str)

args = parser.parse_args()

with open(args.config, 'r') as infile:
    config = json.load(infile)

print(config)

model_name = config['model_name']
os.mkdir("results/{}".format(model_name))

predictor_files_arr = config['predictors']
augment_n = config['augment']['n']
augment_stdev = config['augment']['stdev']

response_file = config['response']['fname']
response_column = config['response']['column']
response_lookback = config['response']['lookback']

dropout_pct = config['model_params']['dropout_pct']
n_layers = config['model_params']['n_layers']
nodes_per_layer=config['model_params']['nodes_per_layer']
model_type=config['model_params']['model_type']

epochs = config['training_params']['epochs']


# create the predictor dataset
def add_lookback_predictors(df, num_days, include_today=True):

    if include_today:
        start = 0
    else:
        start = 1
        num_days = num_days + 1
        
    df = df.sort_values(by=['Date'])
    n = df.shape[0]
    shifted_dfs = [(i, df.iloc[num_days-i:n-i].drop(columns='Date')) for i in range(start, num_days)]
    shifted_dfs_columns = [["{}-{}".format(column, shifted_dfs[j][0]) for column in shifted_dfs[j][1].columns] for j in range(len(shifted_dfs))]
    for j in range(len(shifted_dfs)):
        shifted_dfs[j][1].columns = shifted_dfs_columns[j] 
        shifted_dfs[j][1].index = range(n-num_days)
    print(len(shifted_dfs))
    df_new =  pd.concat([d[1] for d in shifted_dfs], axis=1)
    df_new['Date'] = df.iloc[num_days:]['Date'].values

    return df_new

pred = [add_lookback_predictors(pd.read_csv(f[0]), f[1]+1) for f in predictor_files_arr]

# remove junk columns if they exist
pred_df = reduce(lambda x, y: pd.merge(left=x, right=y, on='Date'), pred)
pred_cols = list(filter(lambda a: not re.match('Unnamed', a), pred_df.columns))
pred_df = pred_df[pred_cols]
pred_df = pred_df.reindex(sorted(pred_df.columns), axis=1)
print("Predictors data")
print(pred_df[['Date']+ list(filter(lambda c: 'keyword_word2vec_york_sum' in c, pred_df.columns))].head())

# add in response data

# load the data
response_df = pd.read_csv(response_file)[[response_column, 'Date']]
response_df.columns = ['response', 'Date']


# create response lookback if necessary
if response_lookback > 0:
    lookback_pred = add_lookback_predictors(response_df, response_lookback, include_today=False)
    response_df = pd.merge(right=response_df, left=lookback_pred, on='Date')

print(response_df.head())

# if classifier, change response variable
if model_type == 'classifier':
    response_df['response'] = response_df.apply(lambda x: 1 if x.response > 0 else 0, axis=1)

# create design matrix
design_mat = pd.merge(left=pred_df, right=response_df, on='Date')

print(design_mat.shape)
print(design_mat.head())

### Create training and test sets
design_test = design_mat.iloc[(596+response_lookback):693]
design_train = design_mat.iloc[response_lookback:595]

Xt = design_test.drop(columns=['Date', 'response']).to_numpy()
yt = design_test['response'].to_numpy() # vol for bonds

X = design_train.drop(columns=['Date', 'response']).to_numpy()
y = design_train['response'].to_numpy()

scale = MinMaxScaler().fit(X)

X_orig = copy.deepcopy(X)
y_orig = copy.deepcopy(y)


for n in range(augment_n):
    random_noise = np.random.normal(0, augment_stdev, X_orig.shape)
    X = np.vstack((X, X_orig + random_noise))
    y = np.hstack((y, y_orig))

X = scale.transform(X)
Xt = scale.transform(Xt)

### Define the model
def create_model(n_predictors, dropout_pct=0, n_layers=3, nodes_per_layer=32, model_type='classifier'):

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dropout(dropout_pct, input_shape=(n_predictors,)))

    # add densely connected layers
    for l in range(n_layers):
        model.add(tf.keras.layers.Dense(nodes_per_layer, activation='relu'))
        model.add(tf.keras.layers.Dropout(dropout_pct))

    #  output layer
    if model_type == 'classifier':
        model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

        # compile the model with adam optimizer and binary cross entropy loss
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        filepath="results/" + model_name + "/weights-improvement-{epoch:02d}-{val_accuracy:.2f}.hdf5"
        checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')

    else:
        model.add(tf.keras.layers.Dense(1, activation='linear'))
        model.compile(loss='mean_squared_error')
        filepath="results/" + model_name + "/weights-improvement-{epoch:02d}-{val_loss:.2f}.hdf5"
        checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')


    return(model, checkpoint)

# create the model
model, checkpoint = create_model(X.shape[1],
                                 dropout_pct=dropout_pct,
                                 n_layers=n_layers,
                                 nodes_per_layer=nodes_per_layer,
                                 model_type=model_type)

history = model.fit(X, y, epochs=epochs, batch_size=128, verbose=1, callbacks=[checkpoint], validation_split=0.3)

if model_type == 'classifier':
    best_epoch = np.argmax(history.history['val_accuracy']) + 1
    best_score = np.max(history.history['val_accuracy'])

else:
    best_epoch = np.argmin(history.history['val_loss']) + 1
    best_score = np.min(history.history['val_loss'])

best_model_path = "results/" + model_name + "/weights-improvement-{0:02d}-{1:.2f}.hdf5".format(best_epoch, best_score)

best_model, _ = create_model(X.shape[1],
                                 dropout_pct=dropout_pct,
                                 n_layers=n_layers,
                                 nodes_per_layer=nodes_per_layer,
                                 model_type=model_type)

best_model.load_weights(best_model_path)

figure, ax = plt.subplots(1, 2, figsize=(20,7))

if model_type == 'classifier':

    # Training plot
    ax[0].plot(range(len(history.history['accuracy'])), history.history['accuracy'], c='blue', label='Training Accuracy')
    ax[0].plot(range(len(history.history['val_accuracy'])), history.history['val_accuracy'], c='red', label='Validation Accuracy')
    ax[0].set_ylabel('Accuracy')
    ax[0].set_xlabel('Epoch')
    ax[0].legend()

    training_acc = history.history['accuracy'][best_epoch - 1]
    validation_acc = history.history['val_accuracy'][best_epoch - 1]

    ax[0].set_title('Training and validation performance\n Training Accuracy: {}, Validation Accuracy: {}'.format(training_acc, validation_acc))        

    # AUC score
    pred_y = best_model.predict(X_orig, verbose=0)
    pred_yt = best_model.predict(Xt, verbose=0)

    y_pred_keras = best_model.predict(Xt).ravel()
    fpr_keras, tpr_keras, thresholds_keras = roc_curve(yt, y_pred_keras)
    auc_keras = auc(fpr_keras, tpr_keras)
    print("Performance: AUC {}, training_accuracy {}, validation_accuracy {}".format(auc_keras, training_acc, validation_acc))
    ax[1].plot(fpr_keras, tpr_keras)
    ax[1].set_title('AUC: {}'.format(auc_keras))
    ax[1].set_ylabel('True Positive Rate')
    ax[1].set_xlabel('False Positive Rate')

else:

    # Training plot
    ax[0].plot(range(len(history.history['loss'])), history.history['loss'], c='blue', label='Training Loss')
    ax[0].plot(range(len(history.history['val_loss'])), history.history['val_loss'], c='red', label='Validation Loss')
    ax[0].set_ylabel('Mean Squared Error Loss')
    ax[0].set_xlabel('Epoch')
    ax[0].legend()

    training_loss = history.history['loss'][best_epoch - 1]
    validation_loss = history.history['val_loss'][best_epoch - 1]
    test_loss = best_model.evaluate(Xt, yt, verbose=0)

    rand_vals = []
    for x in range(100):
        rand_yt = np.array(copy.deepcopy(yt))
        np.random.shuffle(rand_yt)
        rand_vals.append(best_model.evaluate(Xt, rand_yt, verbose=0))

    sorted_vals = np.sort(rand_vals)

    ttest_t, ttest_pval = sp.stats.ttest_1samp(sorted_vals, test_loss)
    print("Performance: tstat {}, pval {}, training_loss {}, validation_loss {}, test_loss {}, random5pc_loss {}, random_mean {}, random95pc_loss {}".format(ttest_t, ttest_pval, training_loss, validation_loss, test_loss, sorted_vals[5], np.mean(rand_vals), sorted_vals[95]))
    ax[0].set_title('Training and validation performance\n Training loss: {0:.6f}, Validation loss: {1:.6f}, Test loss {2:.6f}\nRandomized 5%: {3:.6f}, mean: {4:.6f}, 95%: {5:.6f}\nT-test Statistic: {6:.6f} and p-value: {7:.6f}'.format(training_loss, validation_loss, test_loss, sorted_vals[5], np.mean(rand_vals), sorted_vals[95], ttest_t, ttest_pval)) 

    pred_y = best_model.predict(X_orig, verbose=0)
    pred_yt = best_model.predict(Xt, verbose=0)

    ax[1].set_title('Neural Network Bond Prediction')
    ax[1].set_ylabel('Bond Daily Delta')
    ax[1].set_xlabel('Time (d)')

    #plt.plot(range(len(y_orig)), pred_y, c='b', label='predict')
    #plt.plot(range(len(y_orig)), y_orig, c='r', label='real')
    ax[1].plot(range(len(y_orig),len(yt)+len(y_orig)), pred_yt, c='cornflowerblue', label='predict_test')
    ax[1].plot(range(len(y_orig),len(yt)+len(y_orig)), yt, c='darkorange', label='real_test')
    ax[1].legend()

    ax[1].set_title("Predictions Test Set")

plt.savefig("results/{}/performance.png".format(model_name))
