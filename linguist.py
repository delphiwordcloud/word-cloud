# barebonesLanguageProcessor.py
# author: Michael Odland
# startdate: 01.24.12

# LOG
# last updated: 2.23.12 modland - focused on json file io
# Todo: attach weight to collocations, add on to WordNet so as to include phrases
# Todo: incorporate collocations and n-grams
# transcripts are in xls

print "Loading Natural Language Tool Kit ..."

# for development purposes import everything then hone down to essentials

import json
import nltk
import nltk.data
import os, os.path
from nltk.corpus import stopwords
import string
#from nltk.book import *
from nltk.corpus import wordnet as wn
from nltk import WordNetLemmatizer



def loadRawCorpus(file):
    path = corpusPath()
    nltk.data.load(path+str(file), format = 'raw')


def loadYamlCorpus(path, fname):
    nltk.data.load((path + fname), format = 'yaml')


def corpusPath():
    path = os.path.expanduser('/Users/academy/Documents/PyCharmProjects/django_wordcloud/')
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def jsonToFile(data_string, name): # dictionary in json file out "jsondata"
    data = []
    data.append(data_string)
    f = open((name + ".json"), "w+")
    json.dump(data, f, separators = (',',':'))
    f.flush()


def jsonEncode(dic): # dictionary in json object out
    data = []
    data.append(dic)
    data_string = json.dumps(data, separators = (',',':'))
    print "JSON ENCODED: ", data_string
    return data_string


def synonyms(word): # list of WordNet synonyms for a given word
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas:
            synonyms.append(lemma.name)
    return synonyms


def lemma(words):
    """ lematization is very similar to stemming but more
    akin to synonym replacement. A lemma is a root word and so a valid
    word (rather than a stem) is always returned. If lemmatizer does not
    find a root word it simply returns the original."""
    words2 = []
    for w in words:
        words2.append(lemmatizer.lemmatize(w))
    return words2


#todo: add yaml synonym file and have it be open to the user... each synonym pair has its own line, check out Python Text Processing
#lemmatizer = WordNetLemmatizer()


def context(corpus, dic):
    for w in dic.keys():
        corpus.concordance(w)


def commonPairs(text):
    """collocations are essentially just frequent bigrams, except that we want to pay more attention
    to the cases that involve rare words. In particular, we want to find bigrams that occur more often than
    we would expect based on the frequency of individual words.The collocations() function does this for
    us (we will see how it works later). - NLTK Book Ch1"""
    return text.collocations()


def importantWords(wordcount, vocab):
    # words that have more than N characters and appear more than M times are returned alphabetically
    N = input("get words with more than how many letters?\n:")
    M = input("how many times must a word appear in the text to be of interest?\n:")

    return dict( [ [w, wordcount[w] ]  for w in vocab if len(w) > N and wordcount[w] > M ] ) # check out this cool use of list comprehension


def vocabulary(wordcount):
    # alphabetized vocab is built using list comprehension.
    vocab = sorted( [word for word in wordcount.keys()] )
    return vocab


def pullStops(text):
    """ Stopwords are common words that do not contribute to information retrieval.
    Search engines filter stops to save space in the index.
    so does this program."""
    english_stops = set(stopwords.words('english'))
    text2 = []
    for word in text:
        lower = word.lower()
        if lower.isalpha() and lower not in english_stops:
            text2.append(lower)
    return text2


def process(corpus, path):
    loadRawCorpus(corpus.file.name)
    text      = pullStops(corpus)
    wordcount = FreqDist(text)    # dictionary of words and their count
    vocab     = vocabulary(wordcount)
    important = importantWords(wordcount, vocab)
    pairs     = commonPairs(corpus)

    return wordcount, vocab, important, pairs

#eof
