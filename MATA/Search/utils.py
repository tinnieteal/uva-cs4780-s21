#NLTK package for normalizaiton and tokenization 

import nltk
from nltk.tokenize import word_tokenize  
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import *

p_stemmer = PorterStemmer()

#Please use the NLTK Downloader to obtain the following resources for first time use
# nltk.download('wordnet')
# nltk.download('stopwords')

def nltk_process(text):
    
    #Tokenization
    nltk_tokenList = word_tokenize(text)
    
    #Stemming
    nltk_stemedList = []
    for word in nltk_tokenList:
        nltk_stemedList.append(p_stemmer.stem(word))
    
    #Lemmatization
    wordnet_lemmatizer = WordNetLemmatizer()
    nltk_lemmaList = []
    for word in nltk_stemedList:
        nltk_lemmaList.append(wordnet_lemmatizer.lemmatize(word))
    
    # print("Stemming + Lemmatization")
    # print(nltk_lemmaList)

    #Filter stopword
    filtered_sentence = []  
    nltk_stop_words = set(stopwords.words("english"))
    for w in nltk_lemmaList:  
        if w not in nltk_stop_words:  
            filtered_sentence.append(w)
    
    #Removing Punctuation
    punctuations="?:!.,;"
    for word in filtered_sentence:
        if word in punctuations:
            filtered_sentence.remove(word)
    
    # print(" ")
    # print("Remove stopword & Punctuation")
    return filtered_sentence




