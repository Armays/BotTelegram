# -*-coding:Utf-8 -*

import sys
import time
import random
import datetime
import telepot

from pprint import pprint

def handle(msg):
	
	chat_id = msg['chat']['id']
	from_first_name=msg['from']['first_name']
	from_last_name=msg['from']['last_name']
	from_id=msg['from']['id']
	
	response = bot.getUpdates()
	pprint(response)
	
	try:
		command=msg['text']
		if 'command' in locals():
			if from_first_name=='dyhann' and from_last_name=='armays' :
				bot.sendMessage(chat_id, "Je suis tout à fait d'accord avec toi Diane !")
			elif from_id== 160494965 :
				bot.sendMessage(chat_id, "Tu es rayonnante aujourd'hui Fanny !")
			elif from_first_name=='antoine' and from_last_name=='daigremont' :
				bot.sendMessage(chat_id, "Tu as un super humour Antoine !")
			elif from_id==151270213 :
				bot.sendMessage(chat_id, "Tu as un super cerveau Vincent !")
			elif from_first_name=='Cgallere' and from_last_name=='Cesar' :
				bot.sendMessage(chat_id, "Tu as de belles chaussettes aujourd'hui Yoann !")
	except KeyError:
    # Key is not present
		pass
	
	if 'sticker' in msg.keys() and from_id== 160494965 :
		bot.sendMessage(chat_id, "Très joli sticker Fanny !")
	elif 'sticker' in msg.keys() :
		bot.sendMessage(chat_id, "Bouh c'est pas beau les stickers !")
	elif 'photo' in msg.keys() :
		bot.sendMessage(chat_id, "Quelle belle photo !")
	elif 'document' in msg.keys() :
		bot.sendMessage(chat_id, "Merci pour ce document !")
		chaine=msg['document']['file_name']
		coupure=chaine.split(".")
		for extension in coupure :
			if extension=='doc' or extension=='txt' or extension=='docx' :
				bot.sendMessage(chat_id, "Je vais le lire tout de suite !")
bot = telepot.Bot('148332132:AAGZDbBtAdATqPuTaJFXqnQDgXv9Bn4RDW4')
bot.notifyOnMessage(handle)
print ('I am listening ...')


while 1:
	time.sleep(10)
