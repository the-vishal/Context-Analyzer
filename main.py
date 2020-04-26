import flask
from flask import request, jsonify
from flask_cors import CORS
import json

#approach1 - using Cosine Similarity
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

#approach2 - using word2Vec
from gensim.models import word2vec
import gensim

#FLASK CONFIG
app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)



#HOME
@app.route('/', methods=['GET'])
def home():
    return "<h1><u>NLP based Context Analyzer</u></h1><p>This is a NLP based Context Analyzing tool. <br /> Developer(s) never take responsibility of any cases or results missed. <br /> It is just a tool proposed for helping searcher out there.</p>"


#ANALYZE POST REQ API
@app.route('/analyze', methods=['POST'])
def analyze_context():
    article = request.json.get('article', "")
    testData = request.json.get('testData', "")
    algo = request.json.get('algo', 'dcs')

    if not (article and testData):
        return jsonify("Error: missing values")

    #word2vec
    context = CheckSimilarity(article=article, testdata=testData, algo=algo).relatedContext
    return jsonify(context)



#COSINE SIMILARITY CHECK
class CheckSimilarity(object):
    def __init__(self, article, testdata, algo):
        self.article = article
        self.testdata = testdata
        self.lmtzr = WordNetLemmatizer()

        self.stopWords = stopwords.words('english')+ list('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
        self.stopWords = [' '+i+' ' for i in self.stopWords] 

        if algo =='w2v':
            self.wordmodelfile="H:\softwares\Software Developing\GoogleNews-vectors-negative300-SLIM.bin.gz"                                         
            self.wordmodel= gensim.models.KeyedVectors.load_word2vec_format(self.wordmodelfile, binary=True)

    @staticmethod
    def tokenize_sentences(text):
        sentences = []
        lines = text.split('\n')
        for i in lines:
            sentences.extend(i.split('.'))
        sentences = [i for i in sentences if i.strip()]
        return sentences


    def text_clean(self, text):
        text = ' '+text.lower()+' '
        self.stopWords +=['"',"/","\/"]
        for sw in self.stopWords:
            text = text.replace(sw, " ")
        return text.strip()


    @staticmethod
    def cossim_vectors(v1,v2):
        v1 = v1.reshape(1,-1)
        v2 = v2.reshape(1,-1)
        
        return cosine_similarity(v1,v2)[0][0]


    def w2v(self, s1,s2): 
        if s1==s2:
                return 1.0

        s1words=s1.split()
        s2words=s2.split()
        s1wordsset=set(s1words)
        s2wordsset=set(s2words)
        vocab = self.wordmodel.vocab 
        if len(s1wordsset & s2wordsset)==0:
                return 0.0

        for word in s1wordsset.copy():
                if (word not in vocab):
                        s1words.remove(word)
        for word in s2wordsset.copy():
                if (word not in vocab):
                        s2words.remove(word)

        def get_or_train(s1words, s2words):
            try:
                rate = self.wordmodel.n_similarity(s1words, s2words)
                return rate
            except Exception as ex:
                print(ex)
                self.wordmodel.build_vocab(text, update=True) # update your vocab 
                self.wordmodel.train 
                get_or_train(s1words, s2words)

    @property
    def relatedContext(self, method='dcs'):
        sentences = self.tokenize_sentences(self.article)
        test_sentences = self.tokenize_sentences(self.testdata)
        sentences = list(map(self.text_clean, sentences))
        sentences = list(map(self.lmtzr.lemmatize, sentences))
        test_sentences = list(map(self.text_clean, test_sentences))
        test_sentences = list(map(self.lmtzr.lemmatize, test_sentences))

        if method == 'dcs':
            vectorizer = CountVectorizer().fit_transform(test_sentences+sentences)
            vectors = vectorizer.toarray()
            test_vector = vectors[0]
        else:
            vectors = [' '.join(i) for i in sentences]
            test_vector = ' '.join(test_sentences[0])

        related_context = []
        
        for index, vector in enumerate(vectors[1:]):
            if method=='dcs':
                sim = self.cossim_vectors(test_vector, vector)
            else:
                sim = self.w2v(test_vector, vector)
            if sim>0.4:
                related_context.append(sentences[index])
        return related_context


#APP RUNSERVER
app.run()