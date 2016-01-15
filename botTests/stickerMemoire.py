#!/usr/bin/python3.4
# -*- coding:Utf8 -*
import telepot
import sys
import time
from pprint import pprint
import pickle
from random import choice
token = sys.argv[1]
bot = telepot.Bot(token)
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance2(msg)

    print(msg)

    if content_type is 'sticker':
        with open('stockSticker','rb') as fichier:
            pickler = pickle.Unpickler(fichier)
            f = pickler.load() #renvoie le 1er objet lu
        f += [msg['sticker']['file_id']] #rajoute l'id du sticker envoyé au 1er objet
        sticky = choice(f)
        with open('stockSticker','wb') as fichier:
            pickler = pickle.Pickler(fichier)
            pickler.dump(f) #écrit le dernier sticker envoyé à la fin du fichier

        bot.sendSticker(chat_id, sticky)


bot.notifyOnMessage(handle)
print("listening...")
while 1:
    time.sleep(10)
