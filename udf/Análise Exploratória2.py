#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


from pymongo import MongoClient
import configparser

class Mongo():

    def __init__(self, config_file):
        config = configparser.RawConfigParser()
        config.read(config_file)

        self.server = config.get('mongo', 'server') if 'server' in [i[0] for i in config.items('mongo')] else False
        self.db = config.get('mongo', 'db') if 'db' in [i[0] for i in config.items('mongo')] else False
        self.host = config.get('mongo', 'host') if 'host' in [i[0] for i in config.items('mongo')] else False
        self.port = int(config.get('mongo', 'port')) if 'port' in [i[0] for i in config.items('mongo')] else False
        self.user = config.get('mongo', 'user') if 'user' in [i[0] for i in config.items('mongo')] else False
        self.password = config.get('mongo', 'password') if 'password' in [i[0] for i in config.items('mongo')] else False

        print(self.server)

    def connect(self):
        if self.server == 'True':
            connection_string_basic = "mongodb+srv://{user}:{password}@{host}{port}{db}".format(user=self.user,
                                                                                                   password=self.password,
                                                                                                   host=self.host,
                                                                                                   port="{port}",
                                                                                                   db="{db}")
        else:
            connection_string_basic = "mongodb://{user}:{password}@{host}{port}{db}".format(user=self.user,
                                                                                            password=self.password,
                                                                                            host=self.host,
                                                                                            port="{port}",
                                                                                            db="{db}")

        if self.port:
            connection_string_port = connection_string_basic.format(port=":{}".format(self.port),
                                                                    db="{db}")
        else:
            connection_string_port = connection_string_basic.format(port="",
                                                                    db="{db}")

        if self.db:
            connection_string = connection_string_port.format(db="/{}".format(self.db))
        else:
            connection_string = connection_string_port.format(db="")

        print(connection_string)
        return MongoClient(connection_string)


# In[3]:


mongo = Mongo('config.cfg')
mongo_client = mongo.connect()


# In[4]:


mongo_client.datapop.tweets_to_classify.aggregate([{"$sample":{"size": 3}}])


# In[5]:


sample = {str(obj['_id']): {i:obj[i] for i in obj if i != '_id'} for obj in mongo_client.datapop.tweets_to_classify.aggregate([{'$sample': {'size': 3}}])}
tweets = {str(obj['_id']): {i:obj[i] for i in obj if i != '_id'} for obj in mongo_client.datapop.tweets_classified.find()}


# In[6]:


tweets_list = [tweets[key] for key in tweets.keys()]


# In[7]:


tweets_list


# In[8]:


df_tweets = pd.DataFrame.from_dict(tweets_list)


# In[9]:


df_tweets

from nltk.corpus import stopwords
import nltk
import re


# Lower Case
def lowerCase(doc):
    return  ' '.join([d.lower() for d in doc.split()])


df_tweets['full_text'] = df_tweets['full_text'].apply(lowerCase)
df_tweets['full_text']


# Removendo Stopwords
portuguese_stop_words = stopwords.words('portuguese')
def removeStopwords(doc):
    return ' '.join([w for w in doc.split() if w not in portuguese_stop_words + ['que', 'pra', 'vc', 'vcs', 'q']])
df_tweets['full_text'] = df_tweets['full_text'].apply(removeStopwords)
df_tweets['full_text']


# Removendo Menções
def removeMentions(doc):
    mentions_regex = re.compile('[^@]')
    doc_result = list(filter(lambda tweet: mentions_regex.match(tweet[0]), doc.split()))
    return ' '.join(doc_result)

df_tweets['full_text'] = df_tweets['full_text'].apply(removeMentions)
df_tweets['full_text']

# Removendo links
def removeLinks(doc):
    links_regex = re.compile('^(?!http).*')
    doc_result = list(filter(lambda tweet: links_regex.match(tweet[0]), doc.split()))
    return ' '.join(doc_result)

df_tweets['full_text'] = df_tweets['full_text'].apply(removeLinks)
df_tweets['full_text']


# Removendo Números e placares
def removeNumbersAndScores(doc):
    numbers_regex = re.compile('(([0-9]x[0-9])|(^x$)|(^[0-9]+$))')
    #doc_result = [w for w in doc if token not in list(filter(lambda tweet: numbers_regex.match(tweet[0]), doc.split()))]
    doc_result = [w for w in doc.split() if w not in list(filter(lambda tweet: numbers_regex.match(tweet[0]), doc.split()))]
    return ' '.join(doc_result)

df_tweets['full_text'] = df_tweets['full_text'].apply(removeNumbersAndScores)
df_tweets['full_text']

# Remove Pontuação
def removePontuation(doc):
    #pontuation_regex = re.compile('[^!\.?\:\[\],\{\}\\\/;"\(\)]')
    return re.sub('[!,\.\\\\/?{};\(\)]', '', doc)

df_tweets['full_text'] = df_tweets['full_text'].apply(removePontuation)
df_tweets['full_text'][5]


# Removendo Nome de Times
def removeTeams(doc):
    teams_list = ['fluminense',
                  'flamengo',
                  'botafogo',
                  'vasco',
                  'são paulo',
                  'palmeiras',
                  'santos',
                  'corinthians',
                  'cruzeiro',
                  'atlético mg',
                  'atlético mineiro',
                  'atletico mg',
                  'atletico mineiro',
                  'internacional',
                  'gremio',
                  'chapecoense',
                  'avai',
                  'csa',
                  'bahia',
                  'goias',
                  'athletico pr',
                  'athletico paranaense',
                  'atletico paranaense',
                  'atlético paranaense',
                  'ceara',
                  'fortaleza',
                  'galo'
                 ]

    return re.sub('({})'.format('|'.join(teams_list)), '', doc)

df_tweets['full_text'] = df_tweets['full_text'].apply(removeTeams)
df_tweets['full_text']


# Removendo nomes de jogadores

df_jogadores = pd.read_csv("/Users/thiagotosto/Documents/Pessoal/futpop/docs/caRtola-master/data/2020/2020-medias-jogadores.csv")
lista_jogadores = list(df_jogadores['player_nickname'].apply(lambda x: x.lower())) + ['gabigol', 'babi', 'domenec', 'arão', 'vini', 'leo sena', 'sasha']
lista_jogadores

def removeNames(doc):

    return re.sub('({})'.format('|'.join(lista_jogadores)), '', doc)

df_tweets['full_text'] = df_tweets['full_text'].apply(removeNames)
df_tweets['full_text'][65]
df_tweets['full_text']


# Retirando #hashtags
def removeHashtags(doc):
    doc_result = list(filter(lambda x: not x[0].startswith('#'), doc.split()))
    return ' '.join(doc_result)

df_tweets['full_text'] = df_tweets['full_text'].apply(removeHashtags)
df_tweets['full_text']


# Stemming
from nltk.stem import RSLPStemmer

def stem(doc):
    stemmer = RSLPStemmer()

    doc_result = [stemmer.stem(token) for token in doc.split()]
    return ' '.join(doc_result)

df_tweets['full_text'] = df_tweets['full_text'].apply(stem)


# TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
tf=TfidfVectorizer()
text_tf= tf.fit_transform(df_tweets['full_text'])


# Split Train Test

# TF-IDF
from sklearn.model_selection import train_test_split
TF_X_train, TF_X_test, TF_y_train, TF_y_test = train_test_split(
    text_tf, df_tweets['sentiment'], test_size=0.3, random_state=1)

# MultinomialNB

# TF-IDF
from sklearn.naive_bayes import MultinomialNB
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
# Model Generation Using Multinomial Naive Bayes
clf = MultinomialNB().fit(TF_X_train, TF_y_train)
predicted= clf.predict(TF_X_test)
print("MultinomialNB Accuracy:",metrics.accuracy_score(TF_y_test, predicted))



###rascunho
from sklearn.feature_extraction.text import TfidfVectorizer
tf=TfidfVectorizer()
text_tf= tf.fit_transform(df_tweets['full_text'].append(pd.Series(['que ']), ignore_index=True))

from sklearn.naive_bayes import MultinomialNB
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
# Model Generation Using Multinomial Naive Bayes
clf = MultinomialNB().fit(text_tf[:-1], df_tweets['sentiment'])
predicted= clf.predict(text_tf[-1])
#print("MultinomialNB Accuracy:",metrics.accuracy_score(TF_y_test, predicted))


# In[74]:


predicted


# In[78]:


TF_y_test[:10]


# In[80]:


df_tweets['full_text'][159]


# In[ ]:


predicted


# In[ ]:


def removeLinks(tokens):
    links_regex = re.compile('^(?!http).*')
    return list(filter(lambda tweet: links_regex.match(tweet[0]), tokens))

tokens_no_links = removeLinks(tokens_no_mentions)



# In[ ]:


TF_y_test


# In[ ]:
