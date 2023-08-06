import emoji
import nltk

from nltk.stem import WordNetLemmatizer   
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stopwords
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
analyzer = SentimentIntensityAnalyzer()

punctuations = [',','.','?','~','!','@','#','$','%','^','&','*','(',')','-','+','=','_','[',']','{','}',';',':',"'",'"',"\"",'/']


def sentiment_func(text):
    #text = "I love the color of this product"
    sentiment = analyzer.polarity_scores(text)
    analysis = TextBlob(text)
    tokenized_text = nltk.word_tokenize(text)
    pos_word_list=[]
    neu_word_list=[]
    neg_word_list=[]
    intent_words = []
    for word in tokenized_text:
        word = word.lower()
        if (word not in stopwords) and (word not in punctuations):
            #check first for emojis
            em_flag=0
            for c in word:
                if c in emoji.UNICODE_EMOJI:
                    if (analyzer.polarity_scores(c)['compound']) >-0.1:
                        pos_word_list.append(c)
                    elif (analyzer.polarity_scores(c)['compound']) <= -0.1:
                        neg_word_list.append(c)
                    em_flag=1
            if em_flag==1:
                continue;
            if (analyzer.polarity_scores(word)['compound']) >= 0.1:
                word = lemmatizer.lemmatize(stemmer.stem(word.lower()))
                pos_word_list.append(word)
            elif (analyzer.polarity_scores(word)['compound']) <= -0.1:
                word = lemmatizer.lemmatize(stemmer.stem(word.lower()))
                neg_word_list.append(word)
            else:
                #Intent words search
                cric = lemmatizer.lemmatize(word.lower())
                #if (cric not in stopwords) and (cric not in punctuations):   #####add more special characters in a list
                intent_words.append(cric)
    if sentiment['compound']>=-0.05:
        payload = {"sentiment":"Positive","wordlist":list(set(pos_word_list))}
    else:
        for word in pos_word_list:
            neg_word_list.append('~'+word)
        payload = {"sentiment":"Negative","wordlist":list(set(neg_word_list))}
    payload.update({"intent_words":intent_words})
    return payload


if __name__=="__main__":
    # text = "Thats horribly bad😂😭. 🤔 🙈 😌 💕"
    # text = "I hate the color"
    text = input("Enter a sentence : ")
    print(sentiment_func(text))
