def echo(message):
  markup = types.InlineKeyboardMarkup()
  markupif = types.InlineKeyboardButton("test 'help' callback", callback_data='help')
  markup.add(markupif)
  zigzag.info("Recieved a command!")
  bot.reply_to(message, message.text, reply_markup=markup)

def callecho(call):
  if call.data == "help":
    zigzag.info("Recieved a help call!")
    bot.send_message(call.from_user.id, "Recieved it!")
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False)

def inlineecho(inlinequery):
  if inlinequery.query == "hello":
    zigzag.info("Recieved a query!")
    r = types.InlineQueryResultArticle('1', "Hello dude!", types.InputTextMessageContent('Hi babe!'))
    bot.answer_inline_query(inlinequery.id, [r])
  elif inlinequery.query == "":
    zigzag.info("Recieved an empty query!")
    r = types.InlineQueryResultArticle('1', "Empty query here!", types.InputTextMessageContent("hi mate"))
    bot.answer_inline_query(inlinequery.id, [r])

class plecho:
  patterns = ["^[!/]echo (.*)$"]
  callbacks = ["^help (.*)$", "^help"]
  inlines = ["hel", "DEFAULTQUERY"]
  # At the 'inlines' variable, you can use DEFAULTQUERY to get when there is no queries entered
