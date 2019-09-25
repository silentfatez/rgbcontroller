import logging
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
from Auth import restricted
from DisplayOntoBoard import callingRGB

TOKEN = '<TOKEN>'
updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Move all the commands to another file
class AllCommands:
    ''' This class has all the functions for the /commands'''
    # start is used on start where bot greets user
    def start(update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to BBbot! Enter '/' to see the list of commands available"
                                                                      " and /help to see what the commands do!")

    # help_lah function can be called by user when they want to know what commands are available for them to use
    def help_lah(update, context):
        context.bot.send_message(chat_id = update.message.chat_id, text = "'/set' - Enter text you wish to display on the board"
                                                                          "'/background_colour' - Select background colour (if none selected, default is black)")

    # takes in a message from the user and return the same message
    # def echo(update, context):
    #     context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


    @restricted #by adding this @restricted above the function setText, we only allow specific userIDs to use the setText function
    def setText(update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text="Please enter the message you wish to display on the board")
        # echoes the text
        # dispatcher.add_handler(MessageHandler(Filters.text, AllCommands.echo))

        # we save the message the user sent as displayMessage
        # very buggy now, after calling /set the bot auto Takes '/set' as the message to set
        # then bot will start to echo messages
        displayMessage = update.message.text
        # THIS IS THE BUGGY PART
        context.bot.send_message(chat_id=update.message.chat_id, text="'" + displayMessage + "'")  # try out using dispatcher first
        context.bot.send_message(chat_id=update.message.chat_id, text="Confirm message? (Yes/No)")

        # if user confirms then we will call another function that calls creatergb
        # instantiate a new class instance
        newDisplay = callingRGB()
        newDisplay.callrgb(displayMessage)

# sets up commands for the bot
# echo doesn't stop when u call other commands, so it will end up echo-ing all your messages
class addingHandlers:
    # echo_handler = MessageHandler(Filters.text, AllCommands.echo)
    # dispatcher.add_handler(echo_handler)

    start_handler = CommandHandler('start', AllCommands.start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', AllCommands.help_lah)
    dispatcher.add_handler(help_handler)

    set_handler = CommandHandler('set', AllCommands.setText)
    dispatcher.add_handler(set_handler)

print("Logging...")
updater.start_polling()