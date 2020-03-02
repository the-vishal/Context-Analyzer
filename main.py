import flask
from flask import request, jsonify
from flask_cors import CORS
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords


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
    context = CheckSimilarity(article=article, testdata=testData).relatedContext
    return jsonify(context)



#COSINE SIMILARITY CHECK
class CheckSimilarity(object):
    def __init__(self, article, testdata):
        self.article = article
        self.testdata = testdata

        self.stopWords = stopwords.words('english')+ list('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
        self.stopWords = [' '+i+' ' for i in self.stopWords]                                          

    @staticmethod
    def tokenize_sentences(self, text):
        sentences = []
        lines = text.split('\n')
        for i in lines:
            sentences.extend(i.split('.'))
        sentences = [i for i in sentences if i.strip()]
        return sentences


    def text_clean(self, text):
        text = ' '+text.lower()+' '
        for sw in self.stopWords:
            text = text.replace(sw, " ")
        return text.strip()


    @staticmethod
    def cossim_vectors(self, v1,v2):
        v1 = v1.reshape(1,-1)
        v2 = v2.reshape(1,-1)
        
        return cosine_similarity(v1,v2)[0][0]

    @property
    def relatedContext(self):
        sentences = tokenize_sentences(self.article)
        cleaned_sentences = list(map(self.text_clean, sentences))

        test_sentences = tokenize_sentences(self.testdata)
        cleaned_test_sentences = list(map(self.text_clean, test_sentences))

        vectorizer = CountVectorizer().fit_transform(cleaned_test_sentences+cleaned_sentences)
        vectors = vectorizer.toarray()

        related_context = []

        test_vector = vectors[0]
        for index, vector in enumerate(vectors[1:]):
            cos_sim = cossim_vectors(test_vector, vector)
            if cos_sim>0.4:
                related_context.append(sentences[index])
        return related_context



#APP RUNSERVER
app.run()