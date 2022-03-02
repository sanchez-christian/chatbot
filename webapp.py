#https://www.analyticsvidhya.com/blog/2021/12/creating-chatbot-building-using-python/
from flask import Flask, url_for, render_template, request
from chatterbot import ChatBot
bot = ChatBot("cbot")
bot = ChatBot(
    'cbot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
     logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
    ],
    database_uri='sqlite:///database.sqlite3'
)
#while True:
#    try:
#        bot_input = bot.get_response(input())
#        print(bot_input)
#
#    except(KeyboardInterrupt, EOFError, SystemExit):
#        break
while True:
    try:
        user_input = input()

        bot_response = bot.get_response(user_input)

        print(bot_response)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
from chatterbot.trainers import ListTrainer

trainer = ListTrainer(bot)

trainer.train([
    "Hi! Would you like to order?",
    "Of course, I would be happy to help process your order! What is your name?",
    "#NAME, Would you like to see the menu?",
    "What would you like to order? Please state the name or number.",
    "Will you be paying online or in-store?",
    "Great, #NAME!"
])
app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)
@app.route("/")
def render_main():
    return render_template('home.html')
@app.route("/text")
def render_response():
    return render_template('home.html')

    #The request object stores information about the request sent to the server.
    #args is an ImmutableMultiDict (like a dictionary but can have mutliple values for the same key and can't be changed)
    #The information in args is visible in the url for the page being requested. ex. .../response?color=blue

#if __name__=="__main__":
#    app.run(debug=False)-->

#chatbot = ChatBot('cbot')
#print ("BOT: What is  your name?")
# user_name = input ()
