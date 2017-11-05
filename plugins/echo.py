"""
This is the Test Plugin for the ZigZag project! Everything in here :)
"""

def echo(message):
  # Media messages
  if message.document :
    bot.send_document(message.chat.id, message.document.file_id)
    return
  # Reply Markup! Same as it was before.
  markup = types.InlineKeyboardMarkup()
  markupif = types.InlineKeyboardButton("test 'help' callback", callback_data='help')
  markup.add(markupif)
  # the info() function to print something as an INFO into the console
  zigzag.info("Recieved a command!")
  # send a message to user
  bot.reply_to(message, message.text, reply_markup=markup)
  # Lets checkout the new next_step_handler function in zigzag
  # The function is zigzag.nextstep(message_sent_by_bot, function_name_IN_STRING_FORMAT!)
  # THE FUNCTION NAME "SHOULD" AND "MUST" BE IN "STRING" FORMAT.
  m = bot.send_message(message.from_user.id, "Registered", parse_mode="Markdown")
  zigzag.nextstep(m, "next")
  # Ban a user with zigzag.ban(userid)
  # And unban with zigzag.unban(userid)
  zigzag.unban(message.from_user.id)
  # Get user information with zigzag.getuser(userid)
  print zigzag.getuser(message.from_user.id)['first_name']

# This is the nextstep handler function we define previously in echo()!
def next(message):
  bot.send_message(message.chat.id, "Hi")

# CallBack function for the plugin Echo!
# It should be as this format:
# call<pluginname>() . So in the 'echo'  plugin, it is callecho().
def callecho(call):
  # Call data : 
  if call.data == "help":
    zigzag.info("Recieved a help call!")
    bot.send_message(call.from_user.id, "Recieved it!")
    # Dont forget to answer_callback_query.
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False)

# Inline function for the plugin Echo!
# It should be as this format:
# inline<pluginname() . So in the 'echo' plugin, it is inlineecho().
def inlineecho(inlinequery):
  # Inline data : 
  if inlinequery.query == "hello":
    zigzag.info("Recieved a query!")
    r = types.InlineQueryResultArticle('1', "Hello dude!", types.InputTextMessageContent('Hi babe!'))
    bot.answer_inline_query(inlinequery.id, [r])
  # Empty query ! (A.K.A. DEFAULTQUERY) ||| Its the first thing that appears to a user.
  elif inlinequery.query == "":
    zigzag.info("Recieved an empty query!")
    r = types.InlineQueryResultArticle('1', "Empty query here!", types.InputTextMessageContent("hi mate"))
    bot.answer_inline_query(inlinequery.id, [r])

# The plugin's class! YOU SHOULD DEFINE IT.
# It should be as this format:
# class pl<pluginname> . so in the 'echo' plugin, it is class plecho:
class plecho:
  # REQUIRED FIELD: *patterns* : The text patterns that you need to be passed to the plugin. Use RegEX!
  patterns = ["^[!/]echo (.*)$"]
  # OPTIONAL FIELD: *content_types* : Content type of none-text messages to receive
  content_types = ["document"]
  # OPTIONAL FIELD: *callbacks* : The callback-data patterns that you need to be passed to the plugin.
  callbacks = ["^help (.*)$", "^help"]
  # OPTIONAL FIELD: *inlines* : The inline-query patterns that you need to be passed to the plugin
  # You can use the "DEFAULTQUERY" pattern in the inlines variable, so when there is no query, it will be passed to this plugin.
  inlines = ["hel", "DEFAULTQUERY"]
