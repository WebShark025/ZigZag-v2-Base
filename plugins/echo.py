def echo(message):
  zigzag.info("Im executed!")
  bot.reply_to(message, "Hi")

class plecho:
  patterns = ["^[!/]echo (.*)$"]

