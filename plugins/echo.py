def echo(message):
  markup = types.InlineKeyboardMarkup()
  markupif = types.InlineKeyboardButton("test 'help' callback", callback_data='help')
  markup.add(markupif)
  zigzag.info("Im executed!")
  bot.reply_to(message, "Hi", reply_markup=markup)

def callecho(call):
  if call.data == "help":
    zigzag.info("recieved a help call!")
    bot.send_message(call.from_user.id, "Recieved it!")
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False)

class plecho:
  patterns = ["^[!/]echo (.*)$"]
  callbacks = ["^help (.*)$", "^help"]
