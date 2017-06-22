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
import datetime
import os
import telebot
import re
import sys
import redis
import time as tm
import requests
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

# Define zigzag basics
class Zig:
    def error(self, string):
        self.string = string
        print(textcolor.FAIL + self.string)

zigzag = Zig()
# test purpose:
zig.error("Hi")

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
tm.sleep(5)
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
def message_replier():
  for message in messages:
    for plugin in pllist:
      try:
        exec("p = multiprocessing.Process(target=" + str(plugin) + "(message))")
      except Exception as e:
        zigzag.error("Error")

# Set message handler!
bot.set_update_listener(message_replier)

# Poll! Lets go.
bot.polling(none_stop=True, interval=0, timeout=3)
