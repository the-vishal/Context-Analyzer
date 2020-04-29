'''
Authors:
1.the-vishal : Vishal
2.Vikas92155 : Vikas


*/MIT License

Copyright (c) 2020 the-vishal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import flask
from flask import request, jsonify
from flask_cors import CORS
import json
from urllib.parse import unquote

#approach1 - using Cosine Similarity
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords,wordnet
from itertools import product
import numpy


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
    article = unquote(request.json.get('article', ""))
    testData = unquote(request.json.get('test_data', ""))
    algo = request.json.get('algo', 'wordnet')

    if not (article and testData):
        return jsonify("Error: missing values")

    #word2vec
    context = CheckSimilarity(article=article, testdata=testData, algo=algo).relatedContext
    response = {
                    "match":len(context)>0,
                    "found":len(context),
                    "yourSearch":testData,
                    "resp":context
    }
    return jsonify(response)



#SIMILARITY CHECK
class CheckSimilarity(object):
    def __init__(self, article, testdata, algo):
        self.article = article
        self.testdata = testdata
        self.lmtzr = WordNetLemmatizer()
        self.method = algo

        self.stopWords = stopwords.words('english')+ list('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
        self.stopWords = [' '+i+' ' for i in self.stopWords] 

        if self.method =='w2v':
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


    def getWordnetSimilarity(self, lemm_sent1, lemm_sent2):
        similar_senses = []
        final = []
        for w1 in lemm_sent1:
            similar_synsets =[]
            for w2 in lemm_sent2:
                syns1 = wordnet.synsets(w1)
                syns2 = wordnet.synsets(w2)
                for comb_from_set1, comb_from_set2 in product(syns1, syns2):
                    combination_similarity = wordnet.wup_similarity(comb_from_set1, comb_from_set2)
                    
                    if combination_similarity:
                        similar_senses.append(combination_similarity)

                if similar_senses: 
                    similar_synsets.append(max(similar_senses))

            if similar_senses:
                final.append(max(similar_synsets))

        similarity_index = numpy.mean(final)
        similarity_index = round(similarity_index , 2)
        return similarity_index
    

    def make_sentence_variation(self, tokenize_data):
        sentences_i_have = list(map(self.text_clean, tokenize_data))
        # sentence_types = {}
        # for i in sentences_i_have:
        #     stem_sent = ' '.join(list(map(lemmatizer.lemmatize, i.split(' '))))
        #     lemm_sent = ' '.join([lemmatizer.lemmatize(j, pos="a") for j in  i.split(' ')])
        #     sentence_types.setdefault(i,[]).extend([stem_sent, lemm_sent])
        sentence_types = [list(map(self.lmtzr.lemmatize, i.split(' '))) for i in sentences_i_have]
        return sentence_types


    @property
    def relatedContext(self):
        sentences = self.tokenize_sentences(self.article)
        test_sentences = self.tokenize_sentences(self.testdata)

        lemm_sentences = self.make_sentence_variation(sentences)
        lemm_test_sentences = self.make_sentence_variation(test_sentences)

        if self.method == 'dcs':
            vectorizer = CountVectorizer().fit_transform([' '.join(i) for i in lemm_test_sentences+lemm_sentences])
            vectors = vectorizer.toarray()
            test_vector = vectors[0]

        elif self.method == 'w2v':
            vectors = [' '.join(i) for i in lemm_sentences]
            test_vector = ' '.join(lemm_test_sentences[0])

        else:
            vectors = lemm_sentences
            test_vector = lemm_test_sentences[0]


        related_context = []
        
        for index, vector in enumerate(vectors[1:]):
            if len(vector)>2:
                if self.method=='dcs':
                    sim = self.cossim_vectors(test_vector, vector)
                elif self.method == 'w2v':
                    sim = self.w2v(test_vector, vector)
                else:
                    sim = self.getWordnetSimilarity(test_vector, vector)
                if sim>0.9:
                    related_context.append({"sentence":sentences[index+1], "similarityIndex":sim})
            
            if len(related_context)>2:
                break
        return related_context


#APP RUNSERVER
app.run()