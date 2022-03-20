import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle

with open("intents.json") as file:
    data = json.load(file)

try:
    #if you change anything in your intents.json file, just add an x or something in here so that it doesn't open up your old pickle data and it actually runs through all of this (lines 20-67 or 64) OR you can just delete the old pickle file and delete the old model (lines 69-77 I think) because you'll need to retrain it on that new information that you put in this intents.json file!
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x] )] = 1

    training.append(bag)
    output.append(output_row)


training = numpy.array(training)
output = numpy.array(output)

with open("data.pickle", "wb") as f:
    pickle.dump((words, labels, training, output), f)

tensorflow.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8) #This is a hidden layer. With more and more intents or tags in json file, you want to add more neurons to your hidden layers but 2 hidden layers is typically enough for a problem like this! Refer to Part 3 starting at 5:27 timestamp.
net = tflearn.fully_connected(net, 8) #This is a hidden layer.
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True) #n_epoch=number is the amount of times that it's going to see the same data. Here we're gonna show it the same data 1000 times, but adjust to 2000,5000,100, etc. as seen fit. The more it sees the data, the better it gets a classifying. Refer to Part starting at 10:25 timestamp.
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))] #this is going to create a blank bag of words list and change elements in here to represent if a word exists or doesn't.

    s_words = nltk.word_tokenize(s) #this is a list of tokenized words
    s_words = [stemmer.stem(word.lower()) for word in s_words] #this is going to stem all of our words
    
    for se in s_words:#for loop that will simply generate bag list (line 87)
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1#the 1 represents that the word exists; a 0 represents the contrary

    return numpy.array(bag)#it will take the bag of words (line 87), convert it into a numpy array, and return it to wherever we need that.
    
    
def chat():#we must now write the code that will ask the user for some kind of sentence and then spit out a response; to achieve that, we'll have to start using the model. This is a function we called/named chat (added at the end of our file) in case we want to start chatting with them all as opposed to just training it.
    print("Welcome to Sol y Luna Mexican Restaurant! Please start typing and text 'goodbye' to end the conversation!")
    while True:
        inp = input("You: ")#this shows and indicates that that is what the user is typing or typed.
        if inp.lower() == "goodbye":#This is a wat to get out of the program, this case being if you type 'goodbye' and it will simply break this while loop so that you can end. Otherwise you would just keep goign continuously or else you'd have to close the program.
            break
            
        results = model.predict([bag_of_words(inp, words)])#if the user did not type 'goodbye,' now we're going to turn this input (the words they typed in) into a bag of words (line 87), feed it into the model, and get what the model's response should be. The bag of word (line 87) will create a bag of words with the input that we gave it.
        print(results)
        #results_index = numpy.argmax(results)
        #tag = labels[results_index]
        #print(tag)

chat()