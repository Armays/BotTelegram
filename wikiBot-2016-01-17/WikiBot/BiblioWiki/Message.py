#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

"""
********************************************************************
Ce module Message.py contient toute les fonctions qui vont traiter les \
messages :commandes, envois de fichiers, de stickers, de photos, réponses \
aux commandes, et modifier les paramètres de la base de données UserData.
*******************************************************************
"""

import wikipedia
from random import choice	#Pour le renvoi de stickers au hasard
import pickle
import os					#pour extraire l'extension des fichiers envoyés

def read_UserData() :
	with open("UserData","rb") as fichier :
		monPickler = pickle.Unpickler(fichier)
		DataBank = monPickler.load()
		return(DataBank)
	

def write_UserData(DataBank) :
	with open("UserData","wb") as fichier:
		monPickler = pickle.Pickler(fichier)
		monPickler.dump(DataBank)

def Commande(nouveau,i,chat_id, donneesU, msg,tableauMot, bot):
	if tableauMot[0] == '/help' :
		bot.sendMessage(chat_id,'They call me the Wikiwiki, I can help you make researches on Wikipedia. \nYou can control me by sending these commands: \nEnter /get + researched word to search a word on Wikipedia. \nEnter /language to change the language. \nEnter /rate to rate the bot. \nEnter /start to see your precedent messages. \nEnter /send to send a sticker, photo or document.')
	elif tableauMot[0] == '/get':
		DataBank=read_UserData()
		#SI l'utilisateur n'a pas encore sélectionné sa langue
		if 'language' not in DataBank[i]['parametres'].keys():
			bot.sendMessage(chat_id,'Since it is your first time, you have to choose your language first :)',reply_markup={'keyboard': [['en'], ['fr']], 'force_reply': True})
		#Si l'utilisateur tape /get sans rien après
		elif len(tableauMot) == 1 :
			bot.sendMessage(chat_id, 'What is the word you are looking for ? Enter /get + researched word')
		else :
			DataBank=read_UserData()
			#Réglade de la langue sur wikipedia
			for i,elt in enumerate(DataBank):
				if DataBank[i]['user_id']==msg['from']['id']:
					language=DataBank[i]['parametres']['language']
					wikipedia.set_lang(language)
			try:
				#tableauMot contient tous les mots après le /get
				tableauMot = tableauMot[1:]
				#tableauMot n'est plus un tableau mais une chaine de caractères
				tableauMot = ' '.join(tableauMot[0:])
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
		#force_reply à true pour que la réponse de l'utilisateur soit prise en compte par le bot
		bot.sendMessage(chat_id,'How do you find this bot?', reply_markup={'keyboard': [['Awesome','Great'], ['Average bot','Useless']], 'force_reply': True})
	elif tableauMot[0] == '/start' :
		#Si l'utilisateur tape /start au bot pour la première fois, sans avoir tapé de messages avant.
		if nouveau:
			bot.sendMessage(chat_id,"Hi {} {} and welcome on Wikiwiki. This bot will fetch the information you want directly on Wikipedia.\n type /get and the word you are looking for to have the information. \ntype /language to change the language. \ntype /rate to rate this bot. \ntype /start to have a welcome message. \ntype /send to send a sticker, photo or document. \nThis bot is still in the creating process. New fonctionnalities will appear later. Thank you.".format(msg['from']['first_name'],msg['from']['last_name']))
			bot.sendMessage(chat_id,'Please choose your language :',reply_markup={'keyboard': [['en'], ['fr']], 'force_reply': True})
		else:
			bot.sendMessage(chat_id,"Hi again {} {} !".format(msg['from']['first_name'],msg['from']['last_name']))
			DataBank=read_UserData()
			#Comptage du nombre de messages envoyés par l'utilisateur depuis la première fois où il a parlé au bot
			nb=0
			for message in DataBank[i]['historique'].values():
				nb=nb+1
			bot.sendMessage(msg['chat']['id'],"You sent {} messages :)".format(nb))
			#Transformation du dictionnaire de l'historique utilisateur en liste triée suivant les messages_id. Les messages_id sont des id uniques, et incrémentés par ordre chronologique
			cles_triees=sorted(DataBank[i]['historique'].keys())
			avant_dernier=cles_triees[len(cles_triees)-2]
			avant_dernier_message=DataBank[i]['historique'][avant_dernier]
			#Envoi de l'avant dernier message, en fonction de si c'est un texte, un sticker, une photo ou un document
			if 'text' in avant_dernier_message.keys() :
				bot.sendMessage(chat_id,"Your last message was {}.".format(avant_dernier_message['text']))
			#Contrairement aux fichiers et photos, les stickers n'ont pas besoin d'être enregistrés, ils sont enregistrés dans les bases de données de Telegram
			elif 'sticker' in avant_dernier_message.keys() :
				bot.sendMessage(chat_id,"Your last message was a sticker.")
				bot.sendSticker(chat_id,avant_dernier_message['sticker']['file_id'])
			#Chaque photo envoyée au bot est enregistrée dans le répertoire courant du programme, et son nom est l'id unique attribué à la photo.
			elif 'photo' in avant_dernier_message.keys() :
				bot.sendMessage(chat_id,"Your last message was a photo.")
				#Lors de l'envoi d'une photo, il y a 4 dictionnaires différents avec le meme file_id mais des tailles de photo différentes
				for i,f in enumerate(avant_dernier_message['photo']):
					if f['width']==90:
						with open(f['file_id']+".jpeg","rb") as fichierPhoto:
							bot.sendPhoto(chat_id,fichierPhoto)
			#Chaque document envoyé au bot est enregistré, et on extrait son extension pour pouvoir le réenvoyer. Son nom est son file_id
			elif 'document' in avant_dernier_message.keys() :
				_, extension = os.path.splitext(avant_dernier_message['document']['file_name'])
				with open(avant_dernier_message['document']['file_id']+extension,"rb") as fichier:
					bot.sendDocument(chat_id,fichier)
				bot.sendMessage(chat_id,"Your last message was a document.")
			else :
				bot.sendMessage("Your last message was an emoji.")
	#Cette commande avec le force_reply à true permet que l'envoi de document soit pris en compte par le bot.
	elif tableauMot[0] == '/send':
		bot.sendMessage(chat_id,"Hi you can send me a photo, a document or a sticker if you want",reply_markup={'force_reply': True})
	#Cette commande permet de changer la langue de recherche sur wikipedia
	elif tableauMot[0] == '/language':
		bot.sendMessage(chat_id,'Please choose your language :',reply_markup={'keyboard': [['en'], ['fr']], 'force_reply': True})
#Cette section est incomplète pour le moment. C'est la partie qui s'occupera
#de realiser les commandes entrées par l'utilisateur. Et la réponse de bot
#sera adaptée au contexte et aux préférences de l'utilisateur



def analyseTextNat(i,chat_id,donneesU,msg,tableauMot, bot):
    
#Cette section analysera le texte et le contexte utilisateur
#pour le rendre intelligible pour le reste du programme
#Elle ne remplit aucune fonctionnalité pour le moment
	global note
	rate=True
	language=True
	DataBank=read_UserData()
	cles_triees=sorted(DataBank[i]['historique'].keys())
	avant_avant_dernier=cles_triees[len(cles_triees)-3]
	avant_dernier=cles_triees[len(cles_triees)-2]
	avant_dernier_message=DataBank[i]['historique'][avant_dernier]
	avant_avant_dernier_message=DataBank[i]['historique'][avant_avant_dernier]
	#S'il sagit d'une réponse à /rate
	if avant_dernier_message['text']=='/rate' or (avant_avant_dernier_message['text']=='/rate' and avant_dernier_message['text']!='Awesome' and avant_dernier_message['text']!='Great' and avant_dernier_message['text']!='Average bot' and avant_dernier_message['text']!='Useless'):
		while rate==True:
			#hide_keyboard permet de cacher le clavier car il a été affiché précédemment
			if msg['text'] == 'Awesome':
				bot.sendMessage(chat_id,"Thank you, it's very touching",reply_markup={'hide_keyboard':True})
				note=4
				rate=False
			elif msg['text'] == 'Great':
				bot.sendMessage(chat_id,"Cool, dude",reply_markup={'hide_keyboard':True})
				note=3
				rate=False
			elif msg['text'] == 'Average bot':
				bot.sendMessage(chat_id,"we are gonna work on it",reply_markup={'hide_keyboard':True})
				note=2
				rate=False
			elif msg['text'] == 'Useless':
				bot.sendMessage(chat_id,"That's just mean",reply_markup={'hide_keyboard':True})
				note=1
				rate=False
			else:
				bot.sendMessage(chat_id,'How do you find this bot?', reply_markup={'keyboard': [['Awesome','Great'], ['Average bot','Useless']], 'force_reply': True})
				rate=False
				#On récupère la base de données des utilisateurs dan le fichier UserData
		DataBank=read_UserData()
		total=0
		users=0
		for i,elt in enumerate(DataBank):
			#On sauvegarde le vote dans la base de données
			if DataBank[i]['user_id']==msg['from']['id']:
				DataBank[i]['parametres']['rate']=note
			#On compte le nombre d'utilisateurs ayant voté, et la somme totale des votes
			if 'rate' in DataBank[i]['parametres'].keys():
				users=users+1
				total=total+DataBank[i]['parametres']['rate']
		#Calcul et affiche de la moyenne du vote
		moyenne=total/users
		bot.sendMessage(chat_id,"The average rate of the bot is {} on 4".format(moyenne))
		#Sauvegarde du vote dans les paramètres de la base de données
		write_UserData(DataBank)
		#S'il s'agit d'une réponse à /language, ou /get ou /start pour la première fois, on enregistre la langue dans les paramètres
	elif avant_dernier_message['text'] == '/language' or (avant_avant_dernier_message['text']=='/language' and avant_dernier_message['text']!='fr' and avant_dernier_message['text']!='en'):
		print('test')
		while language==True:
			print('test2')
			if msg['text']!='en' and msg['text']!='fr':
				print('test3')
				bot.sendMessage(chat_id,'Please choose your language :',reply_markup={'keyboard': [['en'], ['fr']], 'force_reply': True})
				language=False
			else:
				DataBank=read_UserData()
				for i,elt in enumerate(DataBank):
					if DataBank[i]['user_id']==msg['from']['id']:
						DataBank[i]['parametres']['language']=msg['text']
						print(DataBank[i]['parametres'])
				write_UserData(DataBank)
				bot.sendMessage(chat_id,"OK thanks ! You can now type your request.", reply_markup={'hide_keyboard':True})
				language=False
	#Si l'utilisateur entre autre chose comme texte que celui escompté
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
		Commande(nouveau,i,chat_id, donneesU, msg,tableauMot, bot)
	else:
		chat_id, donneesU, msg, bot = analyseTextNat(i,chat_id,donneesU,msg,tableauMot, bot)


def Traitement_Sticker(chat_id, msg, bot):
#Cette fonction memorise les stickers reçus et en renvoie un au hasard.
	with open('stockSticker','rb') as fichier:
		pickler = pickle.Unpickler(fichier)
		f = pickler.load()
	f += [msg['sticker']['file_id']]
	sticky = choice(f)
	with open('stockSticker','wb') as fichier:
		pickler = pickle.Pickler(fichier)
		pickler.dump(f)
	bot.sendSticker(chat_id, sticky)
	bot.sendMessage(chat_id,"I can play like this, all day long")

#Cette fonction télécharge tous les documents envoyés
def Traitement_Doc(chat_id,msg,bot):
	_, extension = os.path.splitext(msg['document']['file_name'])
	bot.downloadFile(msg['document']['file_id'],msg['document']['file_id']+extension)
	bot.sendMessage(chat_id,"I don't know how to manage Documents, but I can keep it for you !")

#Cette fonction télécharge toutes les photos envoyées
def Traitement_Photo(chat_id,msg,bot):
	for i,f in enumerate(msg['photo']):
		if f['width']==90:
			bot.downloadFile(f['file_id'],'{}.jpeg'.format(f['file_id']))
	bot.sendMessage(chat_id,"I don't know how to manage Photo, but I can keep it for you !")

"""
Traitement de texte est la première fonction appellée, elle appelle une autre fonction traitement en fonction du contenu du message
"""

def traitementMessage(nouveau,i,DonneesU, msg, bot):
	#chat_id est l'identifiant de la fenêtre de chat : ça peut être une conversation privée ou un groupe
	chat_id = msg['chat']['id']
	if 'text' in msg.keys():
		Traitement_Text(nouveau,i,chat_id,DonneesU,msg, bot)
	elif 'sticker' in msg.keys() :
		Traitement_Sticker(chat_id, msg, bot)
	elif 'photo' in msg.keys() :
		Traitement_Photo(chat_id,msg,bot)
	elif 'document' in msg.keys() :
		Traitement_Doc(chat_id,msg,bot)
