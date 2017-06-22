read -p "Please press ENTER to launch the bot." -n 1 -r
echo " "
#if [[ $REPLY =~ ^[Yy]$ ]]
#then
# while true
#  do
#    python bot.py
#    echo "Bot has crashed! Launching it again."
#  done
#else
python3 bot.py
echo "Bot stopped. exiting"
fi
