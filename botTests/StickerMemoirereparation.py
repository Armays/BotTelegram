#!/usr/bin/python3.4
#-*- coding:Utf8 -*
import pickle

fichier = open('stockSticker','wb')
pickler = pickle.Pickler(fichier)
pickler.dump([])
fichier.close()
