from model.mongo import Mongo
from nltk.corpus import stopwords
import nltk
import re
from nltk.stem import RSLPStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import pandas as pd


class SentimentAnalysis():
    def __init__(self, conf_path='conf/config.cfg'):
        self.mongo_client = Mongo(conf_path).connect()
        self._tasks = [self._lowerCase,
                       self._removeStopwords,
                       self._removeMentions,
                       self._removeLinks,
                       self._removeNumbersAndScores,
                       self._removePontuation,
                       self._removeTeams,
                       self._removeNames,
                       self._removeHashtags,
                       self._stem]
        self._df_tweets = self._getTweets()
        self.sentence = ''
        self.TF_X_train = None
        self.TF_X_test = None
        self.TF_y_train = None
        self.TF_y_test = None
        self.text_tf = None

    def _getTweets(self):
        tweets = {str(obj['_id']): {i:obj[i] for i in obj if i != '_id'} for obj in self.mongo_client.datapop.tweets_classified.find()}

        tweets_list = [tweets[key] for key in tweets.keys()]

        self._df_tweets = pd.DataFrame.from_dict(tweets_list)[['full_text', 'sentiment']]

    def _lowerCase(self, doc):
        return  ' '.join([d.lower() for d in doc.split()])

    def _removeStopwords(self, doc):
        portuguese_stop_words = stopwords.words('portuguese')
        return ' '.join([w for w in doc.split() if w not in portuguese_stop_words + ['que', 'pra', 'vc', 'vcs', 'q']])

    def _removeMentions(self, doc):
        mentions_regex = re.compile('[^@]')
        doc_result = list(filter(lambda tweet: mentions_regex.match(tweet[0]), doc.split()))
        return ' '.join(doc_result)

    def _removeLinks(self, doc):
        links_regex = re.compile('^(?!http).*')
        doc_result = list(filter(lambda tweet: links_regex.match(tweet[0]), doc.split()))
        return ' '.join(doc_result)

    def _removeNumbersAndScores(self, doc):
        numbers_regex = re.compile('(([0-9]x[0-9])|(^x$)|(^[0-9]+$))')
        #doc_result = [w for w in doc if token not in list(filter(lambda tweet: numbers_regex.match(tweet[0]), doc.split()))]
        doc_result = [w for w in doc.split() if w not in list(filter(lambda tweet: numbers_regex.match(tweet[0]), doc.split()))]
        return ' '.join(doc_result)

    def _removePontuation(self, doc):
        #pontuation_regex = re.compile('[^!\.?\:\[\],\{\}\\\/;"\(\)]')
        return re.sub('[!,\.\\\\/?{};\(\)]', '', doc)

    def _removeTeams(self, doc):
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

    def _removeNames(self, doc):
        df_jogadores = pd.read_csv("/Users/thiagotosto/Documents/Pessoal/futpop/docs/caRtola-master/data/2020/2020-medias-jogadores.csv")
        lista_jogadores = list(df_jogadores['player_nickname'].apply(lambda x: x.lower())) + ['gabigol', 'babi', 'domenec', 'arão', 'vini', 'leo sena', 'sasha']

        return re.sub('({})'.format('|'.join(lista_jogadores)), '', doc)

    def _removeHashtags(self, doc):
        doc_result = list(filter(lambda x: not x[0].startswith('#'), doc.split()))
        return ' '.join(doc_result)

    def _stem(self, doc):
        stemmer = RSLPStemmer()

        doc_result = [stemmer.stem(token) for token in doc.split()]
        return ' '.join(doc_result)

    def _applyTasks(self):
        #print(self._df_tweets)

        for task in self._tasks:
            self._df_tweets['full_text'] = self._df_tweets['full_text'].apply(task)

    def _fit(self):
        tf=TfidfVectorizer()
        self.text_tf= tf.fit_transform(self._df_tweets['full_text'])

    def _splitTrain(self):
        self.TF_X_train, self.TF_X_test, self.TF_y_train, self.TF_y_test = train_test_split(self.text_tf[:-1], self._df_tweets['sentiment'][:-1], test_size=0.3, random_state=1)

    def predict(self, sentence):
        #colhendo tweets
        self._getTweets()

        #adicionando tweet em df['full_text']
        self._df_tweets = self._df_tweets.append({'full_text': sentence,
                                'sentiment': 'none'
        }, ignore_index=True)

        #filtrando neutral
        self._df_tweets = self._df_tweets[self._df_tweets['sentiment'] != 'neutral']

        #print(self._df_tweets)

        #aplicando pre processamento de texto
        self._applyTasks()

        #vetorizando texto
        self._fit()

        #separando dataset de treino e dataset de teste
        self._splitTrain()

        #aplicando modelo
        clf = MultinomialNB().fit(self.text_tf[:-1], self._df_tweets['sentiment'][:-1])
        #print(self._df_tweets['full_text'][-1])
        predicted= clf.predict(self.text_tf[-1])

        #print(self._df_tweets)

        return predicted


sentiment = SentimentAnalysis()
sentiment.predict("ruim demais")
