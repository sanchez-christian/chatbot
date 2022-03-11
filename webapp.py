import nltk
import nltk.stem.lancaster import lancaster.Stemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json

with open("intents.json") as file:
    data = json.load(file)

print(data)
