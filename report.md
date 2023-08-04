## dataset
In the provided dataset, there are two vehicle models. The purpose is to make a model predicting its trim and price. The trims are diffirent for both vehicle models. Additionally, all cars are from the USA, thus the models from American modification that limits engine characterisitics. One should note that cars' prices depend on the state where they are being sold.

https://www.iseecars.com/used-car-prices-by-state-study?_isctk=l3vzzw



The dataset was split by model. Separately for each vehicla model was built a ML model. 
## nlp model
Firstly, I build a trim prediction lingustic model (tf-idf + naive bayes) for predicting model. I noticed that the most useful data for that prediction is contained in the colmun "VehFeats". 
## regression model
Secondly, I used obtained Trim and state, history with continues data to make price prediction. For each vehicle model I found the best parameters for the DecitionTreeRegressor algorithm using the GridSearchCV algorithm.  

