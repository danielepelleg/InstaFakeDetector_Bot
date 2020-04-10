#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

import datetime

from utility import readToken
from detector import predict, getPrediction, getProbability

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

ACCOUNT = range(1)

def start(update, context):
    update.message.reply_text(
        'Hi! My name is Instagram Fake Detector Bot.\n\n'
        'I will help you to discover if a Instagram account is fake or not. '
        'Just send me the username of the account you want to verify, and I will give you the answer you search!\n'
        'Anytime, send /cancel to stop talking to me.\n\n')

    return ACCOUNT


def account(update, context):
    if update.message.text == '/cancel':
        return cancel(update,context)
    elif update.message.text == '/start':
        update.message.reply_text('The bot is already active, send me the username of the account you want to verify...')
        return ACCOUNT
    else:
        text = update.message.text
        result = predict(text)
        currentTime = datetime.datetime.utcnow()+datetime.timedelta(hours=1)
        if 5 < currentTime.hour < 12:
            time = 'morning'
        elif 12 <= currentTime.hour < 18:
            time = 'afternoon'
        else:
            time = 'nightly'
        if(result != None):
            prediction = getPrediction(result)
            if (prediction == "real"):
                emote = '✅'
            elif (prediction == "fake"):
                emote = '❌'
            update.message.reply_text(
                'Mhhh, {} is the one you chose...\n\n'
                'This seems to be a {} {} one to me!\n'
                'I\'m quite sure it is. 😉\nIt was fun, send me another one!\n'
                'I\'m always up for some {} training! 👨‍💻'.format(text.lower(), prediction.upper(), emote, time))
        else:
            update.message.reply_text(
                'Mhhh, {} is the one you chose...\n\n'
                'Have you wrote it right? 🤔 '
                'This user doesn\'t exist! But don\'t worry, retry! '
                'I\'m always up for some {} training! 👨‍💻'.format(text.lower(), time))
        return ACCOUNT
    
    

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    logger.info("Starting bot")
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(readToken(), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],

        states={
            ACCOUNT : [MessageHandler(Filters.text, account)]
        },

        fallbacks = [CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()