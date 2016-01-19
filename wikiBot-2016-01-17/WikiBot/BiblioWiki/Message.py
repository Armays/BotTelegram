#!/usr/bin/python3.4
#-*- coding:Utf8 -*
import telepot
import wikipedia
from random import choice
import pickle
import os

def read_UserData() :
	with open("UserData","rb") as fichier :
		monPickler = pickle.Unpickler(fichier)
		DataBank = monPickler.load()
		#print("UserData Message=",DataBank)
		return(DataBank)
	

def write_UserData(DataBank) :
	with open("UserData","wb") as fichier:
		monPickler = pickle.Pickler(fichier)
		monPickler.dump(DataBank)

def Commande(nouveau,i,chat_id, donneesU, msg,tableauMot, bot):
	print("i=",i)
	if tableauMot[0] == '/help' :
		bot.sendMessage(chat_id,'They call me the Wikiwiki, I can help you make researches on Wikipedia. \nYou can control me by sending these commands: \nEnter /get + researched word to search a word on Wikipedia. \nEnter /change to change the language. \nEnter /rate to rate the bot. \nEnter /hello to see your precedent messages. \nEnter /send to send a sticker, photo or document.')
	elif tableauMot[0] == '/get':
		DataBank=read_UserData()
		if 'language' not in DataBank[i]['parametres'].keys():
			bot.sendMessage(chat_id,'Since it is your first time, you have to choose your language first :)',reply_markup={'keyboard': [['en'], ['fr']], 'force_reply': True})
		elif len(tableauMot) == 1 :
			bot.sendMessage(chat_id, 'What is the word you are looking for ? Enter /get + researched word')
		else :
			DataBank=read_UserData()
			for i,elt in enumerate(DataBank):
				if DataBank[i]['user_id']==msg['from']['id']:
					language=DataBank[i]['parametres']['language']
					wikipedia.set_lang(language)
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
				bot.sendMessage(chat_id,'This request sends several responses, what did uou mean ?  :')
				bot.sendMessage(chat_id,e.options)
	elif tableauMot[0] == '/rate':
		bot.sendMessage(chat_id,'How do you find this bot?', reply_markup={'keyboard': [['Awesome','Great'], ['Average bot','Useless']], 'force_reply': True})
	elif tableauMot[0] == '/hello' :
		if nouveau:
			bot.sendMessage(chat_id,"Hi {} {} and welcome on Wikiwiki. This bot will fetch the information you want directly on Wikipedia.\n Tape /get and the word you are looking for to have the information. \nTape /change to change the language. \nTape /rate to rate this bot. \nTape /hello to have a welcome message. \nTape /send to send a sticker, photo or document. \nThis bot is still in the creating process. New fonctionnalities will appear later. Thank you.".format(msg['from']['first_name'],msg['from']['last_name']))
		else:
			bot.sendMessage(chat_id,"Hi again {} {} !".format(msg['from']['first_name'],msg['from']['last_name']))
			DataBank=read_UserData()
			nb=0
			for message in DataBank[i]['historique'].values():
				#print(message)
				if 'text' in message.keys():
					nb=nb+1
			bot.sendMessage(msg['chat']['id'],"You have sent {} messages :)".format(nb))
			cles_triees=sorted(DataBank[i]['historique'].keys())
			avant_dernier=cles_triees[len(cles_triees)-2]
			avant_dernier_message=DataBank[i]['historique'][avant_dernier]
			if 'text' in avant_dernier_message.keys() :
				bot.sendMessage(chat_id,"Your last message was {}.".format(avant_dernier_message['text']))
			elif 'sticker' in avant_dernier_message.keys() :
				bot.sendMessage(chat_id,"Your last message was a sticker.")
				bot.sendSticker(chat_id,avant_dernier_message['sticker']['file_id'])
			elif 'photo' in avant_dernier_message.keys() :
				bot.sendMessage(chat_id,"Your last message was a photo.")
				#print(avant_dernier_message['photo']['file_id'])
				#print(avant_dernier_message['photo']['file_id']+".jpeg")
				for i,f in enumerate(avant_dernier_message['photo']):
					if f['width']==90:
						with open(f['file_id']+".jpeg","rb") as fichierPhoto:
							bot.sendPhoto(chat_id,fichierPhoto)
			elif 'document' in avant_dernier_message.keys() :
				_, extension = os.path.splitext(avant_dernier_message['document']['file_name'])
				with open(avant_dernier_message['document']['file_id']+extension,"rb") as fichier:
					bot.sendDocument(chat_id,fichier)
				bot.sendMessage(chat_id,"Your last message was a document.")
			else :
				bot.sendMessage("Your last message was an emoji.")
	elif tableauMot[0] == '/send':
		bot.sendMessage(chat_id,"Hi you can send me a photo, a document or a sticker if you want",reply_markup={'force_reply': True})
	elif tableauMot[0] == '/change':
		bot.sendMessage(chat_id,'Please choose your language :',reply_markup={'keyboard': [['en'], ['fr']], 'force_reply': True})
#Cette section est incomplète pour le moment. C'est la partie qui s'occupera
#de realiser les commandes entrées par l'utilisateur. Et la réponse de bot
#sera adaptée au contexte et aux préférences de l'utilisateur



def analyseTextNat(chat_id,donneesU,msg,tableauMot, bot):
    
#Cette section analysera le texte et le contexte utilisateur
#pour le rendre intelligible pour le reste du programme
#Elle ne remplit aucune fonctionnalité pour le moment
	global note
	#print(donneesU)
	#print((msg['message_id']))
	#messPrec = donneesU['historique'][(msg['message_id'])-2]    #Attention: Les messages ID vont de deux en deux parce que chacune des réponses du bot sont considérées comme des messages de la part de Telegram.
	if msg['text'] == 'Awesome' or msg['text'] == 'Great' or msg['text'] == 'Average bot' or msg['text'] == 'Useless':
		if msg['text'] == 'Awesome':
			bot.sendMessage(chat_id,"Thank you, it's very touching",reply_markup={'hide_keyboard':True})
			note=4
		elif msg['text'] == 'Great':
			bot.sendMessage(chat_id,"Cool, dude",reply_markup={'hide_keyboard':True})
			note=3
		elif msg['text'] == 'Average bot':
			bot.sendMessage(chat_id,"we are gonna work on it",reply_markup={'hide_keyboard':True})
			note=2
		elif msg['text'] == 'Useless':
			bot.sendMessage(chat_id,"That's just mean",reply_markup={'hide_keyboard':True})
			note=1
		DataBank=read_UserData()
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
		bot.sendMessage(chat_id,"The average rate of the bot is {} on 4".format(moyenne))
		write_UserData(DataBank)
	elif msg['text'] == 'fr' or msg['text'] == 'en':
		DataBank=read_UserData()
		for i,elt in enumerate(DataBank):
			if DataBank[i]['user_id']==msg['from']['id']:
				DataBank[i]['parametres']['language']=msg['text']
				print(DataBank[i]['parametres'])
		write_UserData(DataBank)
		bot.sendMessage(chat_id,"OK thanks ! You can now tape your request.", reply_markup={'hide_keyboard':True})
	else:
		bot.sendMessage(chat_id,"That makes no sense",reply_markup={'hide_keyboard':True})
	return(chat_id,donneesU,tableauMot, bot)



def Traitement_Text(nouveau,i,chat_id, donneesU, msg, bot):
#Separe deux cas possibles. Si l'utiisateur a mis un / devant son texte ou non
#Le message ne sera pas traité de la même façon. Si c'est du texte naturel, 
#le texte sera envoyé à la fonction traitement de texte naturel. Si c'est une
#commande, cette fonction executera la commande sans ce soucier du contexte.
	tableauMot = msg['text'].split(" ")
	if(tableauMot[0][0] == '/'):
		print("i=",i)
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

def Traitement_Doc(chat_id,msg,bot):
	_, extension = os.path.splitext(msg['document']['file_name'])
	bot.downloadFile(msg['document']['file_id'],msg['document']['file_id']+extension)
	bot.sendMessage(chat_id,"I don't know how to manage Documents")

def Traitement_Photo(chat_id,msg,bot):
	for i,f in enumerate(msg['photo']):
		if f['width']==90:
			bot.downloadFile(f['file_id'],'{}.jpeg'.format(f['file_id']))
	bot.sendMessage(chat_id,"I don't know how to manage Photo, but I keep it for you !")

"""
Traitement de texte est la première fonction appellée, elle appelle une autre fonction traitement en fonction du contenu du message
"""

def traitementMessage(nouveau,i,DonneesU, msg, bot):
	ID = msg['from']['id']
	chat_id = msg['chat']['id']
	if 'text' in msg.keys():
		print("i=",i)
		Traitement_Text(nouveau,i,chat_id,DonneesU,msg, bot)
	elif 'sticker' in msg.keys() :
		Traitement_Sticker(chat_id, msg, bot)
	elif 'photo' in msg.keys() :
		Traitement_Photo(chat_id,msg,bot)
	elif 'document' in msg.keys() :
		Traitement_Doc(chat_id,msg,bot)
	
