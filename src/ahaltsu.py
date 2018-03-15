#!/usr/bin/env python
# -*- coding: utf-8 -*-

import calendar
from datetime import datetime

import yaml
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="I don't understand this order")


def exercises(bot, update):
    content = None

    with open('src/routine.yml', 'r') as config:
        try:
            content = yaml.load(config)
            print(yaml.dump(content))
        except yaml.YAMLError as error:
            print(error)
            raise

    today = calendar.day_name[datetime.now().weekday()].lower()
    today_routine = content[today]['exercises']
    current = '{:-^49}\n'.format(' [ TRX ] ')

    for exercise in today_routine:
        if exercise == 'rest':
            current += 'Rest day :)'
            break

        for e in exercise:
            current_exercise = '{}\nSeries: {}\nRepeticiones: {}\n{:-^50}\n'.format(
                exercise[e]['description'], exercise[e]['series'], exercise[e]['replays'], '- + -')

            current += current_exercise

    update.message.reply_text(current)


def main():
    updater = Updater('YOUR-TOKEN')
    dispatcher = updater.dispatcher

    echo_handler = MessageHandler(Filters.text, echo)
    routine_handler = CommandHandler('routine', exercises)

    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(routine_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
