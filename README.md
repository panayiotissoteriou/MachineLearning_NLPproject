# MachineLearning_NLPproject
Movie genre classification using Natural Language Processing

In this project we used a variety of NLP methods to classify movies according to their genres, based on the summaries of their plots. We collected and preprocessed the movie summaries and associated genres, we employed word embedding approaches and machine learning methods, namely Support Vector Machine and Logistic Regression, for the task of text classification.

Key tasks:
- For description-specific preprocessing, the WordNet Lemmatizer from NLTK was used.
- To convert movie descriptions into 100-dimensional vectors, the genism module and KeyedVectors.load_word2vec were used.
- Pre-trained embeddings from enwiki_20180420 (window=5, iteration=10, negative=15) were used to obtain 100-dimensional vectors corresponding to single words.

The datasets used, containing movie genres and summaries, were obtained from the published database of Carnegie Mellon University (Bamman D., O'Connor B., Smith N. (2013). “Learning Latent Personas of Film Characters” ACL. https://aclanthology.org/P13-1035.pdf).
