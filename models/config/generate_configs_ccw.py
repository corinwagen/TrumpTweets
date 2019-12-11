#!/usr/bin/python
import json

predictors = ["../tweets/data/keyword_word2vec_predictors.by_day.csv",
              "../tweets/data/frequent_handles.by_day.csv",
              "../tweets/data/word2vec_doc_embeddings.by_date.csv",
              "../tweets/data/topic_model_simple_weights.by_date.csv",
              "../tweets/data/sentiment.by_day.csv",
              "../tweets/data/metadata.by_day.csv",
              "../tweets/data/keywords.by_day.csv",
              "../tweets/data/embedded_topic_model_topic_scores.by_day.csv"]

predictor_lookbacks = range(5)

#responses = ["../stocks/amer_stocks_delta.csv"]
responses = ["../miscdata/golddata.csv"]
response_columns = "delta"
response_lookbacks = range(5)

dropout_pcts = [0.0, 0.2, 0.3, 0.4, 0.5]
n_layers = [3]
nodes_per_layer = [32]
epochs=[100]
model_types = ['classifier', 'regressor']

# first order with each predictor
i = 0
for predictor in predictors:
   for predictor_lookback in predictor_lookbacks:
      for response_lookback in response_lookbacks:
         for dropout_pct in dropout_pcts:
            for model_type in model_types:
               config = { "model_name" : "model_{}".format(i),
                          "predictors" : [[predictor, predictor_lookback]],
               "augment": {
                            "n": 50,
                            "stdev": 0.2
                          },
               "response": {
                            "fname": responses[0],
                            "column": response_columns,
                            "lookback": response_lookback
                           },
               "model_params" : {
                                "dropout_pct": dropout_pct,
                                "n_layers": n_layers[0],
                                "nodes_per_layer": nodes_per_layer[0],
                                "model_type": model_type
                               },
               "training_params" : {
                                "epochs" : epochs[0]
                                 }
                        }
               with open("model_{}.json".format(i), 'w') as fp:
                   json.dump(config, fp)
               print(["bond_model_{}.json".format(i), predictor, predictor_lookback, response_lookback, dropout_pct, model_type, responses[0], response_columns, n_layers[0], nodes_per_layer[0], epochs[0]])
               i += 1

