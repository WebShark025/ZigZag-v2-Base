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
from shutil import copyfile
from telebot import types



# Check for CONFIG file and LOCALE file
if not os.path.exists("config.py"):
  copyfile("data/config.default.py", "config.py")
if not os.path.exists("locale.py"):
  copyfile("data/locale.default.py", "locale.py")

# Connect to Redis database
redisserver = redis.StrictRedis(host='localhost', port=6379, db=0)

# Set *default encoding*
reload(sys)  
sys.setdefaultencoding("utf-8")

# Load config and locale file into the system. 
execfile("locale.py")
execfile("config.py")

# Start the bot
bot = telebot.TeleBot(TOKEN)

# Load plugins
for plugin in enabled_plugins:
  try:
    execfile("plugins/" + plugin + ".py")
    print("Plugin enabled successfully: " + plugin)
  except Exception as ex:
    print("Could enable plugin: " + plugin + ". Error:")
    print(ex)

print("Bot launched successfully. Launch time: " + str(time))

# Set message handler!
bot.set_update_listener(message_replier)

# Poll! Lets go.
bot.polling(none_stop=True, interval=0, timeout=3)
