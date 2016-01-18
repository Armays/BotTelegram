#!/usr/bin/python3.4
# -*- coding:Utf8 -*
import telepot
import sys
import time
from pprint import pprint
import pickle
#token = sys.argv[1]
token=''
bot = telepot.Bot(token)
def handle(msg):
	
	content_type, chat_type, chat_id = telepot.glance2(msg)
	if content_type is 'photo':
		pprint(msg['photo'])
		for i,f in enumerate(msg['photo']):
			print(f['file_id'])

			bot.downloadFile(f['file_id'],'C:/Users/Diane/newpicture.jpeg')
			with open('C:/Users/Diane/newpicture.jpeg','rb') as fichierPhoto:
				bot.sendPhoto(chat_id,fichierPhoto)
	bot.sendMessage(chat_id,'merci')



bot.notifyOnMessage(handle)
print("listening...")
while 1:
	time.sleep(10)
