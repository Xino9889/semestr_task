from dto.base import db
from poll.config import questions
from poll.anket import Anket
from telebot import types, telebot
import json

bot = telebot.TeleBot("5916072464:AAGxUrQi9-pdWhQ1JXnz3e9ghvR4twClGsI")
anket = Anket(questions)

def gen_markup(options, k):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    l = [types.InlineKeyboardButton(x, callback_data=f'{{"questionNumber": {k},"answerText": "{x}"}}')
                                    for x in options]
    markup.add(*l)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    req = call.data.split('_')
    print(req)
    json_string = json.loads(req[0])
    k = json_string['questionNumber'] + 1
    answer = json_string['answerText']
    db.add_answer(chat_id=call.message.chat.id, question_id=k-1, answer=answer)
    if k == anket.length:
        user_answers = [answer["A_" + str(i)] for answer in db.get_user_answers(call.message.chat.id) for i in range(anket.length)]
        score = anket.add_answers(user_answers)
        text = anket.get_final_text(score)
        db.print_users_data()
        return bot.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 text=text)

    button_column = anket.config[k]['options']
    qtype = anket.config[k].get('type')
    if qtype == 'opened':
        msg = bot.send_message(chat_id=call.message.chat.id, text=anket.get_question(k))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(msg, process_open_answer, k)
    elif qtype == 'number':
        msg = bot.send_message(chat_id=call.message.chat.id, text=anket.get_question(k))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(msg, process_number_answer, k)
    else:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=anket.get_question(k),
                              reply_markup=gen_markup(button_column, k))

def process_open_answer(message, k):
    db.add_answer(chat_id=message.chat.id, question_id=k, answer=message.text)
    k += 1

    if k == anket.length:
        user_answers = [answer["A_" + str(i)] for answer in db.get_user_answers(message.chat.id) for i in range(anket.length)]
        score = anket.add_answers(user_answers)
        text = anket.get_final_text(score)
        bot.send_message(chat_id=message.chat.id, text=text)
    else:
        button_column = anket.config[k]['options']
        qtype = anket.config[k].get('type')
        if qtype == 'opened':
            msg = bot.send_message(chat_id=message.chat.id, text=anket.get_question(k))
            bot.register_next_step_handler(msg, process_open_answer, k)
        elif qtype == 'number':
            msg = bot.send_message(chat_id=message.chat.id, text=anket.get_question(k))
            bot.register_next_step_handler(msg, process_number_answer, k)
        else:
            bot.send_message(chat_id=message.chat.id, text=anket.get_question(k), reply_markup=gen_markup(button_column, k))

def process_number_answer(message, k):
    db.add_answer(chat_id=message.chat.id, question_id=k, answer=message.text)
    k += 1

    if k == anket.length:
        user_answers = [answer["A_" + str(i)] for answer in db.get_user_answers(message.chat.id) for i in range(anket.length)]
        score = anket.add_answers(user_answers)
        text = anket.get_final_text(score)
        bot.send_message(chat_id=message.chat.id, text=text)
    else:
        button_column = anket.config[k]['options']
        qtype = anket.config[k].get('type')
        if qtype == 'opened':
            msg = bot.send_message(chat_id=message.chat.id, text=anket.get_question(k))
            bot.register_next_step_handler(msg, process_open_answer, k)
        elif qtype == 'number':
            msg = bot.send_message(chat_id=message.chat.id, text=anket.get_question(k))
            bot.register_next_step_handler(msg, process_number_answer, k)
        else:
            bot.send_message(chat_id=message.chat.id, text=anket.get_question(k), reply_markup=gen_markup(button_column, k))

@bot.message_handler(commands=['start'])
def start(message):
    k = 0
    button_column = anket.config[k]['options']
    db.insert_user(name=message.chat.username, chat_id=message.chat.id, total_score=0)
    bot.send_message(chat_id=message.chat.id, text="Привет, братан! Ответь на мои вопросы по вселенной Шрека дабы понимать что ты ровный парень")
    bot.send_message(chat_id=message.chat.id, text=anket.get_question(k), reply_markup=gen_markup(button_column, k))

bot.polling()
