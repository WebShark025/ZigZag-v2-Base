# -*- coding: utf-8 -*-

# ##################################
#          ZigZag  v2 !!           #
# Based on The ZigZag Project v2 ! #
# Author: WebShark25               #
# (Mohammad Arshia Seyyed Shakeri) #
####################################
#   Author's Website:              #
#            www.webshark25.ir     #
#                                  #
#    iTeam's Website:              #
#             www.iteam-co.ir      #
####################################
#                                  #
#       Copyright @2017-2019       #
#        LICENSED UNDER MIT        #
#                                  #
####################################


# Imports
import multiprocessing
import datetime
import urllib
import os
import telebot
import re
import json
import sys
import redis
import time as tm
import requests
import inspect
import traceback
import thread
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
    def log_message(self, sender, string):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        nextstep = "({}) ".format(instephandler[str(sender)][1]) if str(sender) in instephandler else ""
        print(textcolor.RESET + "‎[{} MESSAGE] {}{} => {}‎".format(now, nextstep, sender, string))
    def log_callback(self, sender, string):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        print(textcolor.RESET + "‎[{} CALLBAC] {} => {}‎".format(now, sender, string))
    def error(self, string):
        self.string = string
        stack = inspect.stack()
        pluginname = stack[1][0].f_code.co_name
        print(textcolor.FAIL + "[" + pluginname + "] " + str(self.string) + textcolor.RESET)
        return True
    def info(self, string):
        self.string = string
        stack = inspect.stack()
        pluginname = stack[1][0].f_code.co_name
        print(textcolor.RESET + "[" + pluginname + "] " + self.string + textcolor.RESET)
        return True
    def nextstep(self, message, function):
        try:
          self.message = message
          self.function = function
          stack = inspect.stack()
          pluginname = stack[1][0].f_code.co_name
          uid = message.chat.id
          instephandler[str(uid)] = [pluginname, function]
          redisserver.hset("zigzag:nextsteps", message.chat.id, function)
          bot.register_next_step_handler(message, nextstephandler)
          return True
        except Exception as e:
          print(e)
          return False
    def ban(self, userid):
        self.userid = userid
        redisserver.sadd('zizgzag:banlist', int(self.userid))
        bot.send_message(int(self.userid), "شما از ربات بن شدید!", parse_mode="Markdown")
        zigzag.info("User {} got banned from the bot!".format(userid))
        return True
    def unban(self, userid):
        self.userid = userid
        try:
          redisserver.srem('zigzag:banlist', int(self.userid))
        except:
          pass
        zigzag.info("User {} got unbanned from the bot!".format(userid))
        bot.send_message(int(self.userid), "شما از ربات آنبن شدید!", parse_mode="Markdown")
        return True
    def getuser(self, userid):
        self.userid = userid
        userinfo = redisserver.hget('zigzag:userdata', self.userid)
        return eval(userinfo)

zigzag = Zig()

# Print greeting
print(textcolor.OKBLUE + "#########################################")
print("#########################################")
print("The ZigZag Project v2!")
print("#########################################")
print("#########################################")
print("iTeam Proudly Presents!")
print("Copyright 2017-2019 @WebShark25")
print("#########################################")
print("#########################################")
tm.sleep(1)
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
    print(textcolor.RESET + "[zigzag_main] " + textcolor.OKBLUE + "Plugin enabled successfully: " + plugin)
    pllist.append(plugin)
  except Exception as ex:
    print(textcolor.FAIL + "Could not enable plugin: " + plugin + ". Error:")
    print(textcolor.WARNING + str(ex))

# Choose ONLY if you are using mongodb. Will be fully introduced in v3
#execfile('objects_mongodb.py')
print(textcolor.RESET + "[zigzag_main] " + textcolor.OKGREEN + "Objects loaded.")

# PLACE FOR ANY ADDITIONAL CODES TO LOAD SUCH AS DAEMONS.
# RUN LIKE THIS:
#thread.start_new_thread(funcname, ())

time = datetime.datetime.now()
print(textcolor.OKGREEN + "\n\nBot launched successfully. Launch time: " + str(time) + textcolor.RESET)

# Define Next Step Handler function
def nextstephandler(message):
  zigzag.log_message(message.from_user.id, message.text)
  message.from_user = load_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                                 False, message.from_user.username)
  redisserver.hdel("zigzag:nextsteps", message.chat.id)
  if not message.text:
    message.text = ""
  redisserver.hdel("zigzag:nextsteps", message.chat.id)
  if (message.text == "/cancel") or ("بازگشت" in message.text):
    try:
      del instephandler[str(message.from_user.id)]
    except:
      pass
    try:
      profile(message)
    except Exception as e:
      print(e)
    return
  try:
    #pluginname = instephandler[str(message.from_user.id)][0]
    funcname = instephandler[str(message.from_user.id)][1]
    if funcname == instephandler[str(message.from_user.id)][1]:
      del instephandler[str(message.from_user.id)]
    exec("thread.start_new_thread( " + str(funcname) + ", (message, ) )")
    # In this line, it conflicts with the next nextstep (if registered) thats why a doublecheck is needed
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    zigzag.error("Error registering next step: " + str(e) + "\nInfo :" + ''.join(traceback.format_tb(exc_tb)))


# Define message handler function.
def message_replier(messages):
  for message in messages:
    zigzag.log_message(message.from_user.id, message.text)
    #message.from_user = load_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.is_bot, message.from_user.username)
    sent = False
    userid = message.from_user.id
    banlist = redisserver.sismember('zigzag:banlist', userid)
    if banlist:
      return
    """
    if not redisserver.get("coinsell:lastactivity:{}".format(userid)):
      if bot.get_chat_member("@CHATID", userid).status == "left":
        try:
          redisserver.hset("strtmsg", message.from_user.id, message.text)
        except:
          pass
        print(message.from_user.id, message.text)
        txt = "you should join blah blah blah channel"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("♻ بررسی عضویت", callback_data='barresi'))
        try:
            bot.send_message(userid, txt, reply_markup=markup)
        except:
            pass
        return
      else:
        redisserver.setex("coinsell:lastactivity:{}".format(userid), 600, 600)""" # Ozviat ejbari for those who know what it is
    allmembers = list(redisserver.smembers('zigzag:members'))
    if str(userid) not in allmembers:
      if "group" in message.chat.type:
        return
      redisserver.sadd('zigzag:members', userid)
      userinfo = str(message.from_user)
      redisserver.hset('zigzag:userdata', userid, userinfo)
    if message.text:
      if message.text == "/cancel" or "/start" in message.text or "بازگشت" in message.text:
        redisserver.hdel("zigzag:nextsteps", message.chat.id)
        start(message)
        return
    # Check if is the message in in_step_handler?
    if str(message.from_user.id) in instephandler:
      return
    if redisserver.hget("zigzag:nextsteps", message.chat.id):
      exec("thread.start_new_thread( " + str(redisserver.hget("zigzag:nextsteps", message.chat.id)) + ", (message, ) )")
      redisserver.hdel("zigzag:nextsteps", message.chat.id)
      return
    elif message.text:
      # Else, Try to find a regex match in all plugins.
      for plugin in pllist:
        exec("pln = pl" + plugin + ".patterns")
        try:
          for rgx in pln:
            rlnumber = re.compile(rgx)
            args = message.text
            if rlnumber.search(args):
              sent = True
              exec("thread.start_new_thread( " + str(plugin) + ", (message, ) )")
        except Exception as e:
          exc_type, exc_obj, exc_tb = sys.exc_info()
          zigzag.error("Error: " + str(e) + "\nInfo :" + ''.join(traceback.format_tb(exc_tb)))
    else :
      for plugin in pllist:
        try :
          exec("content_types = pl" + plugin + ".content_types")
          try:
            if message.content_type in content_types :
              exec("thread.start_new_thread( " + str(plugin) + ", (message, ) )")
          except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            zigzag.error("Error: " + str(e) + "\nInfo :" + ''.join(traceback.format_tb(exc_tb)))
        except :
          pass
    if not sent:
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      markup.add("بازگشت به منوی اصلی")
      if message.photo:
        txt = """⭕️ کاربر گرامی!

⏱ درخواست شما منقضی شده است. لطفا، عملیات را مجددا از سر بگیرید."""
      else:
        txt = "⭕️ متوجه دستورت نشدم. لطفا از اول شروع کن 👇"
      bot.send_message(message.chat.id, txt, reply_markup=markup)

# Set message handler!
bot.set_update_listener(message_replier)

# Define callback data.
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
  #call.from_user = load_user(call.from_user.id, call.from_user.first_name, call.from_user.last_name, call.from_user.is_bot, call.from_user.username)
  call.message.from_user = call.from_user
  zigzag.log_callback(call.from_user.id, call.data)
  """if call.data == "barresi":
    if bot.get_chat_member("@CHATID", call.from_user.id).status == "left":
      bot.answer_callback_query(call.id, "شما در یکی از کانالهل عضو نشده یید! لطفا دکمه JOIN را فشار دهید.", show_alert=True)
      return
    else:
      bot.edit_message_text(call.message.text, call.message.chat.id, call.message.message_id)
      redisserver.setex("coinsell:lastactivity:{}".format(call.from_user.id), 600, 600)
      call.message.text = redisserver.hget("strtmsg", call.from_user.id)
      start(call.message)
      return"""
  if call.message:
    _hash = "anti_flood:user:" + str(call.from_user.id)
    max_time = 10
    msgs = 0
    if redisserver.get(_hash):
      msgs = int(redisserver.get(_hash))
      max_msgs = 15  # msgs in
      max_time = 10  # seconds
      if msgs > max_msgs:
        return
    redisserver.setex(_hash, max_time, int(msgs) + 1)
    for plugin in pllist:
      try:
        exec("pln = pl" + plugin + ".callbacks")
      except:
        continue
      try:
        for rgx in pln:
          rlnumber = re.compile(rgx)
          args = call.data
          if rlnumber.search(args):
            exec("thread.start_new_thread( call" + str(plugin) + ", (call, ) )")
            break
      except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        zigzag.error("Error: " + str(e) + "\nInfo :" + ''.join(traceback.format_tb(exc_tb)))

# Define inline function
@bot.inline_handler(func=lambda query: True)
def inline_hand(inlinequery):
  for plugin in pllist:
    try:
      exec("pln = pl" + plugin + ".inlines")
    except:
      continue
    try:
      for rgx in pln:
        rlnumber = re.compile(rgx)
        args = inlinequery.query
        if rlnumber.search(args):
          exec("p = multiprocessing.Process(target=inline" + str(plugin) + "(inlinequery))")
          p.start()
          break
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      zigzag.error("Error: " + str(e) + "\nInfo :" + ''.join(traceback.format_tb(exc_tb)))
    if len(inlinequery.query) is 0:
      for rgx in pln:
        if rgx == "DEFAULTQUERY":
          exec("p = multiprocessing.Process(target=inline" + str(plugin) + "(inlinequery))")
          p.start()

# Poll! Lets go.
bot.polling(none_stop=True, interval=0, timeout=3)
