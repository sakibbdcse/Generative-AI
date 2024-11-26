import os
import re
import string,time
import json
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
import emoji
import pandas as pd
idmDatasetPath = "./dataSet/IMDBDataset.csv"
# read csv file
df = pd.read_csv(idmDatasetPath)
# lower case all data
df['review'] = df['review'].str.lower()
# remove the html tags from the text
def removeHtmlTag(text):
    pattern = re.compile('<.*?>')
    return pattern.sub(r'',text)

df['review'] = df['review'].apply(removeHtmlTag)
# remove url from text
def removeUrl(text):
    pattern = re.compile(r'https?://\S+|www\.\S+')
    return pattern.sub(r'',text)
df['review'] = df['review'].apply(removeUrl)

# remove punctuation fuction

def removePunctuation(text):
    exclude = string.punctuation
    # this is a remove punctuation loop it's time take long
    # for char in exclude:
    #     text = text.replace(char,'')
    # here the better solution for this
    return text.translate(str.maketrans('','',exclude))
df['review'] = df['review'].apply(removePunctuation)
# detact abbreviations social media conversion word detected fuction
def abbreviationsConversion(text):
    slang = './dataSet/slang.json'
    with open(slang,'r+') as file:
        chatWord = json.load(file)
        newText = []
        for w in text.split():
            if w.upper() in chatWord:
                newText.append(chatWord[w.upper()])
            else:
                newText.append(w)
    return " ".join(newText)

# print(abbreviationsConversion('ASAP'))

# handle incorrect text 
increct_text = "hey how you fell lock like this time and dictonary and how wuld you know this dictionary"
textCorection = TextBlob(increct_text)
textCorection.correct().string
# print(text)

# stop word using nltk
# nltk.download('stopwords')

def removeStopWords(text):
    newText = []
    for word in text.split():
        if word in stopwords.words('english'):
            newText.append('')
        else:
            newText.append(word)
    x = newText[:]
    newText.clear()
    return ' '.join(x)

# df['review'] = df['review'].apply(removeStopWords)

# emoji handly
def removeEmoji(text):
    emojiPattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # Emoticons
                               u"\U0001F300-\U0001F5FF"  # Symbols & Pictographs
                               u"\U0001F680-\U0001F6FF"  # Transport & Map Symbols
                               u"\U0001F700-\U0001F77F"  # Alchemical Symbols
                               u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               "]+", flags=re.UNICODE)
    return emojiPattern.sub(r'', text)

# print(removeEmoji("love this emoji 😊"))
print(emoji.demojize("love this emoji 😊"))
# print(df['review'][7])