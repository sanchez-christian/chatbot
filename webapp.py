from flask import Flask, url_for, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
bot = ChatBot(
    'cbot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
     logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch',
    ],
    database_uri='sqlite:///database.sqlite3'
)

print("Type something to begin...")

trainer = ListTrainer(bot)

trainer.train([
    "Hi! Would you like to order?",
    "Of course, I would be happy to help process your order! What is your name?",
    "#NAME, Would you like to see the menu?",
    "What would you like to order? Please state the name or number.",
    "Will you be paying online or in-store?",
    "Great, #NAME!"
])
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
    #The request object stores information about the request sent to the server.
    #args is an ImmutableMultiDict (like a dictionary but can have mutliple values for the same key and can't be changed)
    #The information in args is visible in the url for the page being requested. ex. .../response?color=blue

#if __name__=="__main__":
#    app.run(debug=False)-->

#chatbot = ChatBot('cbot')
#print ("BOT: What is  your name?")
# user_name = input ()
