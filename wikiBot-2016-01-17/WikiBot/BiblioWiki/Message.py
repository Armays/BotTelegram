#!/usr/bin/python3.4
#-*- coding:Utf8 -*
import telepot
import wikipedia
from random import choice
import pickle

def Commande(nouveau,i,chat_id, donneesU, msg,tableauMot, bot):
	if tableauMot[0] == '/help' :
		bot.sendMessage(chat_id,'Enter /get + researched word to search a word on Wikipedia, enter /change to change the lang, enter /rate + researched word to rate the bot, enter /hello to see your precedent messages, enter /send to send a sticker, photo or document.')
	elif tableauMot[0] == '/get':
		if nouveau:
			bot.sendMessage(chat_id,'Which lang do you chose ?',reply_markup={'keyboard': [['en'], ['fr']], 'force_reply': True})
		if len(tableauMot) == 1 :
			bot.sendMessage(chat_id, 'What is the word you are looking for ? Enter /get + researched word')
		else :
			with open("UserData","rb") as fichier :
				monPickler = pickle.Unpickler(fichier)
				DataBank = monPickler.load()
			for i,elt in enumerate(DataBank):
				if DataBank[i]['user_id']==msg['from']['id']:
					lang=DataBank[i]['parametres']['lang']
					wikipedia.set_lang(lang)
			try:
				tableauMot = tableauMot[1:]
				print(tableauMot)
				tableauMot = ' '.join(tableauMot[0:])
				print(tableauMot)
				page = wikipedia.page(tableauMot)
				bot.sendChatAction(chat_id, 'typing')
				bot.sendMessage(chat_id,wikipedia.summary(tableauMot, sentences=1))
				bot.sendChatAction(chat_id, 'typing')
				bot.sendMessage(chat_id,page.url)
			except wikipedia.exceptions.PageError :
				bot.sendMessage(chat_id, 'There is no result corresponding to your research')
			except wikipedia.exceptions.DisambiguationError as e:
				bot.sendMessage(chat_id,'This request sens several responses, what did uou mean ?  :')
				bot.sendMessage(chat_id,e.options)
	elif tableauMot[0] == '/rate':
		bot.sendMessage(chat_id,'How do you find this bot?', reply_markup={'keyboard': [['Awesome','Great'], ['average bot','It sucks']], 'force_reply': True})
		
	elif tableauMot[0] == '/hello' :
		if nouveau:
			bot.sendMessage(msg['chat']['id'],"Hi {} {} and welcome on Wikiwiki. This bot will fetch the information you want directly on Wikipedia. Tape /get and the word you are looking for to have the information. Tape /change to change the lang. Tape /rate to rate this bot. Tape /hello to have a welcome message. Tape /send to send a sticker, photo or document. This bot is still in the creating process. New fonctionnalities will appear later. Thank you.".format(msg['from']['first_name'],msg['from']['last_name']))
		else:
			bot.sendMessage(msg['chat']['id'],"Hi again {} {} ! Here are your precedent messages : ".format(msg['from']['first_name'],msg['from']['last_name']))
			with open("UserData","rb") as fichier :
				monPickler = pickle.Unpickler(fichier)
				DataBank = monPickler.load()
				for message in DataBank[i]['historique'].values():
					print(message)
					if 'text' in message.keys():
						bot.sendMessage(msg['chat']['id'],message['text'])
	elif tableauMot[0] == '/send':
		bot.sendMessage(msg['chat']['id'],"Hi you can send me a photo, a document or a sticker if you want",reply_markup={'force_reply': True})
	elif tableauMot[0] == '/change':
		bot.sendMessage(chat_id,'Which lang do you chose ?',reply_markup={'keyboard': [['en'], ['fr']], 'force_reply': True})
#Cette section est incomplète pour le moment. C'est la partie qui s'occupera
#de realiser les commandes entrées par l'utilisateur. Et la réponse de bot
#sera adaptée au contexte et aux préférences de l'utilisateur



def analyseTextNat(chat_id,donneesU,msg,tableauMot, bot):
    
#Cette section analysera le texte et le contexte utilisateur
#pour le rendre intelligible pour le reste du programme
#Elle ne remplit aucune fonctionnalité pour le moment
	global note
	print(donneesU)
	print((msg['message_id']))
	#messPrec = donneesU['historique'][(msg['message_id'])-2]    #Attention: Les messages ID vont de deux en deux parce que chacune des réponses du bot sont considérées comme des messages de la part de Telegram.
	if msg['text'] == 'Awesome' or msg['text'] == 'Great' or msg['text'] == 'average bot' or msg['text'] == 'It sucks':
		if msg['text'] == 'Awesome':
			bot.sendMessage(chat_id,"Thank you, it's very touching",reply_markup={'hide_keyboard':True})
			note=4
		elif msg['text'] == 'Great':
			bot.sendMessage(chat_id,"Cool, dude",reply_markup={'hide_keyboard':True})
			note=3
		elif msg['text'] == 'average bot':
			bot.sendMessage(chat_id,"we are gonna work on it",reply_markup={'hide_keyboard':True})
			note=2
		elif msg['text'] == 'It sucks':
			bot.sendMessage(chat_id,"That's just mean",reply_markup={'hide_keyboard':True})
			note=1
		with open("UserData","rb") as fichier :
			monPickler = pickle.Unpickler(fichier)
			DataBank = monPickler.load()
			total=0
			users=0
			for i,elt in enumerate(DataBank):
				if DataBank[i]['user_id']==msg['from']['id']:
					DataBank[i]['parametres']['rate']=note
				if 'rate' in DataBank[i]['parametres'].keys():
					print(DataBank[i]['parametres']['rate'])
					users=users+1
					total=total+DataBank[i]['parametres']['rate']
			moyenne=total/users
			bot.sendMessage(chat_id,"La moyenne générale du bot est de {} sur 4".format(moyenne))
		with open("UserData","wb") as fichier:
			monPickler = pickle.Pickler(fichier)
			monPickler.dump(DataBank)
	elif msg['text'] == 'fr' or msg['text'] == 'en':
		with open("UserData","rb") as fichier :
			monPickler = pickle.Unpickler(fichier)
			DataBank = monPickler.load()
			for i,elt in enumerate(DataBank):
				if DataBank[i]['user_id']==msg['from']['id']:
					DataBank[i]['parametres']['lang']=msg['text']
		with open("UserData","wb") as fichier:
			monPickler = pickle.Pickler(fichier)
			monPickler.dump(DataBank)
		bot.sendMessage(chat_id,"ok thanks !", reply_markup={'hide_keyboard':True})
	else:
		bot.sendMessage(chat_id,"That's make no sense",reply_markup={'hide_keyboard':True})
	



	return(chat_id,donneesU,tableauMot, bot)



def Traitement_Text(nouveau,i,chat_id, donneesU, msg, bot):
#Separe deux cas possibles. Si l'utiisateur a mis un / devant son texte ou non
#Le message ne sera pas traité de la même façon. Si c'est du texte naturel, 
#le texte sera envoyé à la fonction traitement de texte naturel. Si c'est une
#commande, cette fonction executera la commande sans ce soucier du contexte.
	tableauMot = msg['text'].split(" ")
	if(tableauMot[0][0] == '/'):
		Commande(nouveau,i,chat_id, donneesU, msg,tableauMot, bot)
	else:
		chat_id, donneesU, msg, bot = analyseTextNat(chat_id,donneesU,msg,tableauMot, bot)


def Traitement_Sticker(chat_id, msg, bot):
#Cette fonction memorise les stickers reçus et en renvoie un au hasard.
	with open('stockSticker','rb') as fichier:
		pickler = pickle.Unpickler(fichier)
		f = pickler.load()
	f += [msg['sticker']['file_id']]
	print(f)
	sticky = choice(f)
	with open('stockSticker','wb') as fichier:
		pickler = pickle.Pickler(fichier)
		pickler.dump(f)
	bot.sendSticker(chat_id, sticky)
	bot.sendMessage(chat_id,"I can play like this, all day long")

def Traitement_Doc(chat_id,bot):
	bot.sendMessage(chat_id,"I don't know how to manage Documents")

def Traitement_Photo(chat_id,bot):
	bot.sendMessage(chat_id,"I don't know how to manage Photo")

"""
Traitement de texte est la première fonction appellée, elle appelle une autre fonction traitement en fonction du contenu du message
"""

def traitementMessage(nouveau,i,DonneesU, msg, bot):
	ID = msg['from']['id']
	chat_id = msg['chat']['id']
	if 'text' in msg.keys():
		Traitement_Text(nouveau,i,chat_id,DonneesU,msg, bot)
	elif 'sticker' in msg.keys() :
		Traitement_Sticker(chat_id, msg, bot)
	elif 'photo' in msg.keys() :
		Traitement_Photo(chat_id,bot)
	elif 'document' in msg.keys() :
		Traitement_Doc(chat_id,bot)
	
