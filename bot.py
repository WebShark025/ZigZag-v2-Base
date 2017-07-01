####################################
# The ZigZag Project v2 !          #
# Author: WebShark25               #
# (Mohammad Arshia Seyyed Shakeri) #
####################################
#                                  #
# Copyright @2017 iTeam Product    #
#                                  #
####################################


# Imports
import multiprocessing
import datetime
import os
import telebot
import re
import json
import sys
import redis
import time as tm
import requests
import inspect
from shutil import copyfile
from telebot import types


# Define color codes
class textcolor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\x1b[0m'

# Load Empty Dicts/Lists/Etc. 
instephandler = {}

# Define zigzag basics
class Zig:
    def error(self, string):
        self.string = string
        stack = inspect.stack()
        pluginname = stack[1][0].f_code.co_name
        print(textcolor.FAIL + "[" + pluginname + "] " + self.string + textcolor.RESET)
        return True
    def info(self, string):
        self.string = string
        stack = inspect.stack()
        pluginname = stack[1][0].f_code.co_name
        print(textcolor.RESET + "[" + pluginname + "] " + self.string + textcolor.RESET)
        return True
    def nextstep(self, message, function):
        self.message = message
        self.function = function
        stack = inspect.stack()
        pluginname = stack[1][0].f_code.co_name
        uid = eval(str(message))['chat']['id']
        instephandler[str(uid)] = pluginname
        bot.register_next_step_handler(message, function)
        return True
    def ban(self, userid):
        self.userid = userid
        redisserver.sadd('zigzag:banlist', int(self.userid))
        bot.send_message(int(self.userid), "You are banned from the bot!", parse_mode="Markdown")
        return True
    def unban(self, userid):
        self.userid = userid
        try:
          redisserver.srem('zigzag:banlist', int(self.userid))
        except:
          pass
        bot.send_message(int(self.userid), "You are unbanned from the bot!", parse_mode="Markdown")
        return True



zigzag = Zig()
# test purpose:
#zigzag.error("Hi")

# Print greeting
print(textcolor.OKBLUE + "#########################################")
print("#########################################")
print("The ZigZag Project v2!")
print("#########################################")
print("#########################################")
print("iTeam Proudly Presents!")
print("Copyright 2017 @WebShark25")
print("#########################################")
print("#########################################")
tm.sleep(2)
print("\n\n\n\n\n\n")

# Enabled plugins list.
pllist = []

# Check for CONFIG file and LOCALE file
if not os.path.exists("config.py"):
  copyfile("data/config.default.py", "config.py")
if not os.path.exists("locale.py"):
  copyfile("data/locale.default.py", "locale.py")

# Load config and locale file into the system.
execfile("locale.py")
execfile("config.py")

# Check for the TOKEN (is it right?)
stats = requests.get("https://api.telegram.org/bot{}/getMe".format(config['token'])).json()
if stats["ok"] == True:
  pass
else:
  print(textcolor.FAIL + "Error launching the bot: Wrong TOKEN id!")
  print("Error code: " + str(stats['error_code']) + " \nError description: " + stats['description'])
  print("Please edit the " + textcolor.WARNING + "config.py" + textcolor.FAIL + " file and enter your bot's TOKENID in it." + textcolor.RESET)
  exit()

# Connect to Redis database
redisserver = redis.StrictRedis(host='localhost', port=6379, db=0)

# Set *default encoding*
reload(sys)  
sys.setdefaultencoding("utf-8")

# Start the bot
bot = telebot.TeleBot(config['token'])

# Load plugins
for plugin in enabled_plugins:
  try:
    execfile("plugins/" + plugin + ".py")
    print(textcolor.OKBLUE + "Plugin enabled successfully: " + plugin)
    pllist.append(plugin)
  except Exception as ex:
    print(textcolor.FAIL + "Could not enable plugin: " + plugin + ". Error:")
    print(textcolor.WARNING + str(ex))

time = datetime.datetime.now()
print(textcolor.OKGREEN + "Bot launched successfully. Launch time: " + str(time) + textcolor.RESET)

# Define message handler function.
def message_replier(messages):
  for message in messages:
    userid = message.from_user.id
    banlist = redisserver.sismember('zigzag:banlist', userid)
    if banlist:
      return
    allmembers = list(redisserver.smembers('zigzag:members'))
    if userid not in allmembers:
      redisserver.sadd('zigzag:members', userid)
      userinfo = str(message.from_user)
      redisserver.hadd('zigzag:userdata', userid, userinfo)
    # Check if is the message in in_step_handler?
    if str(message.from_user.id) in instephandler:
#      exec("p = multiprocessing.Process(target=" + str(plugin) + "(message))")
#      p.start()
      # Whats going on onthe top line?:| IDK
      del instephandler[str(message.from_user.id)]
      return
    else:
      # Else, Try to find a regex match in all plugins.
      for plugin in pllist:
        exec("pln = pl" + plugin + ".patterns")
        try:
          for rgx in pln:
            rlnumber = re.compile(rgx)
            args = message.text
            if rlnumber.search(args):
              exec("p = multiprocessing.Process(target=" + str(plugin) + "(message))")
              p.start()
        except Exception as e:
          zigzag.error("Error: " + str(e))

# Set message handler!
bot.set_update_listener(message_replier)

# Define callback data.
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
  if call.message:
    for plugin in pllist:
      exec("pln = pl" + plugin + ".callbacks")
      try:
        for rgx in pln:
          rlnumber = re.compile(rgx)
          args = call.data
          if rlnumber.search(args):
            exec("p = multiprocessing.Process(target=call" + str(plugin) + "(call))")
            p.start()
      except Exception as e:
        zigzag.error("Error: " + str(e))

# Define inline function
@bot.inline_handler(func=lambda query: True)
def inline_hand(inlinequery):
  for plugin in pllist:
    exec("pln = pl" + plugin + ".inlines")
    try:
      for rgx in pln:
        rlnumber = re.compile(rgx)
        args = inlinequery.query
        if rlnumber.search(args):
          exec("p = multiprocessing.Process(target=inline" + str(plugin) + "(inlinequery))")
          p.start()
    except Exception as e:
      zigzag.error("Error: " + str(e))
    if len(inlinequery.query) is 0:
      for rgx in pln:
        if rgx == "DEFAULTQUERY":
          exec("p = multiprocessing.Process(target=inline" + str(plugin) + "(inlinequery))")
          p.start()

# Poll! Lets go.
bot.polling(none_stop=True, interval=0, timeout=3)
