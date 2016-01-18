# coding: utf-8
import sys
import time
import telepot
import wikipedia

def handle(msg):
	wikipedia.set_lang("fr")
	content_type, chat_type, chat_id = telepot.glance2(msg)
	print (content_type, chat_type, chat_id)
	if content_type == 'sticker' :
		bot.sendMessage(chat_id,'Pardon ?')
	if content_type == 'text' :
		command = msg['text'].split()
		print (command)
		if command[0] == '/help' :
			bot.sendMessage(chat_id,'Taper /get suivi du mot recherché')
            
		if command[0] == '/get' :
			if len(command) == 1 :
				bot.sendMessage(chat_id, 'Quel est le mot recherché ? Taper /get suivi du mot recherché')
			else :
				try:
					command = command[1:]
					print(command)
					command = ' '.join(command[0:])
					print(command)
					page = wikipedia.page(command)
					bot.sendChatAction(chat_id, 'typing')
					bot.sendMessage(chat_id,wikipedia.summary(command, sentences=1))
					bot.sendChatAction(chat_id, 'typing')
					bot.sendMessage(chat_id,page.url)
				except wikipedia.exceptions.PageError :
					bot.sendMessage(chat_id, 'Il n\'y a aucun résultat correspondant à la requête.')
				except wikipedia.exceptions.DisambiguationError as e:
					bot.sendMessage(chat_id,'Cette requête renvoie plusieurs résultats, est ce que vous vouliez dire  :')
					bot.sendMessage(chat_id,e.options)

bot = telepot.Bot('')
bot.notifyOnMessage(handle)
print ('Listening ...')


while 1:
	time.sleep(10)
