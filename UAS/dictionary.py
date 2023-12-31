import pandas as pd

# Define a dictionary for classification
classification_dict = {
    'programming_languages': ['python', 'java', 'scala', 'c++', 'swift', 'go', 'golang', 'matlab', 'javascript', 'r', 'sql', 'julia', 'sas'],
    'machine learning task': ['supervised learning', 'unsupervised learning', 'semi-supervised learning', 'reinforcement learning', 'transfer learning', 'active learning', 
                         'classification', 'regression','clustering', 'dimentionality reduction', 'anomaly detection', 'association rule learning', 'sequence mining', 
                         'recommendation systems'],
    'machine learning algorithm' : ['linear regression', 'polynomial regression', 'ridge regression', 'lasso regression', 'elasticnet regression', 'logistic regression', 
                                    'k-nearest neighbors', 'support vector machines','svm', 'decision trees', 'random forest', 'naive bayes', 'principal component analysis','pca',  
                                    'k-means clustering', 'hierarchical clustering', 'DBSCAN', 'bagging', 'boosting', 'adaboost', 'gradient boosting', 'xgboost', 'artificial neural networks', 
                                    'convolutional neural networks','cnn', 'recurrent neural networks', 'rnn', 'q-learning', 'state-action-reward-state-action', 'deep q', 
                                    'association rules', 'apriori', 'eclat', 'anomaly detection', 'isolation forest', 'natural language processing', 'lgbm'],
    'deep learning task': ['image classification', 'object detection', 'semantic segmentation', 'instance segmentation', 'text generation', 'machine translation', 
                      'speech recognition', 'text-to-speech', 'speech-to-text', 'synthesis', 'style transfer', 
                      'super resolution', 'generative modeling'],
    'database':['mysql', 'postgresql', 'mongodb', 'cassandra', 'redis', 'elasticsearch', 'sqlite', 'mariadb', 'oracle', 'sql server', 'db2', 'teradata', 'sybase', 
                'bigquery', 'hive', 'hbase', 'neo4j', 'influxdb', 'couchbase', 'riak', 'couchdb', 'dynamodb', 'azure sql', 'google cloud sql', 'amazon rds', 'amazon redshift', 
                'amazon aurora', 'firebase', 'airtable', 'ibm informix', 'vertica', 'greenplum', 'snowflake', 'sap hana', 'clickhouse', 'cockroachdb', 'firebird', 'interbase', 
                'mimer sql', 'nuodb', 'percona', 'pervasive psql', 'r:base', 'rasdaman', 'realm', 'sap iq', 'sap adaptive server', 'soliddb', 'splice machine', 'sqream db', 
                'timescale db', 'yugabytedb'],
    'cloud platform': ['aws', 'gcp', 'azure', 'ibm', 'alibaba', 'oracle', 'sap'],
    'statistics': ['mean', 'median', 'mode', 'range', 'standard deviation', 'variance', 'quartile', 'interquartile range',
    'probability', 'random variable', 'probability distribution', 'probability density function', 'cumulative distribution function', 'expected value', 'variance', 'independence',
    'hypothesis testing', 'confidence interval', 'p value', 'null hypothesis', 'alternative hypothesis', 'regression analysis', 'correlation', 'anova',
    'simple random sampling', 'stratified random sampling', 'cluster sampling', 'systematic sampling', 'sampling error', 'sampling bias', 'sample size',
    'data cleaning', 'data transformation', 'data normalization', 'outlier detection', 'feature engineering', 'dimensionality reduction', 'data visualization',
    'experimental group', 'control group', 'randomized controlled trial', 'cross sectional study', 'longitudinal study', 'observational study', 'confounding variable',
    't test', 'chi squared test', 'anova', 'mann whitney u test', 'wilcoxon signed rank test', 'kruskal wallis test', 'fisher exact test',
    'bayesian inference', 'prior probability', 'posterior probability', 'bayesian network', 'markov chain monte carlo', 'bayesian credibility interval', 'bayesian updating']
}