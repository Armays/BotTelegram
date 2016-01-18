#!/usr/bin/python3.4
#-*- coding:Utf8 -*

"""
*****************************************************************************************
Fichier main: contient l'enchainement logique des traitements,\
faisant appel aux modules présent dans la bibliothèque locale.\
Pour toute information sur les rôles des fonctions appelées,\
référez vous aux commentaires présents pour chaque fonction dans\
le modules concerné.\

Pour le moment, toute les opérations sont effectuées en interne de la fonction "messMan"\
(messMan = Messages Management)\
Dans l'avenir le bot exécutera des commandes externes à cette fonction. En particulier\
pour le mécanisme d'apprentissage qui devra se faire parallèlement aux traitements\
des messages.\

Pour toute information supplémentaire n'hésitez pas à nous contacter à l'adresse suivante\
*****************************************************************************************
"""
import telepot      #Bibliothèque distante: Communicatiion avec l'API de Télégram
from BiblioWiki.Pedia import *
from BiblioWiki.UserM import *
from BiblioWiki.Message import *
#import sys          #Bibliothèque systeme, pour la prise d'arguments entre autres
import time


#token = sys.argv[1] #Entrée du token en argument = Confidentialité/Code transportable
token ="135994390:AAEF-1YrQ6vxELe-xRDqyZndRgbI0_8Uino"
bot = telepot.Bot(token)

def messMan(msg):                               #Reception du message
	wikipedia.set_lang("fr")                    #Donne des résultat plus cohérents pour des recherches francaises
	#global DonneesU                 
	nouveau,i,DonneesU = identification(msg,bot)     #Renvoie toute les données Utilisateur
	traitementMessage(nouveau,i,DonneesU,msg,bot)   #Traite le message
    
#On pourra rajouter après ici l'appel des modules pour l'apprentissage
#du robot.


bot.notifyOnMessage(messMan)   #Reception du message suivant
print("listening...")   #Permet de savoir que le programme est activé en console
while 1:
	time.sleep(10)
