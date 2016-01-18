#!/usr/bin/python3.4
#-*- coding:Utf8 -*
import pickle
with open("UserData","wb") as fichier:
    monPickler = pickle.Pickler(fichier)
    monPickler.dump([])

fichier = open('stockSticker','wb')
pickler = pickle.Pickler(fichier)
pickler.dump([])
fichier.close()
