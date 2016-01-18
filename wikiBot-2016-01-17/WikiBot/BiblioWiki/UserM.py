#!/usr/bin/python3.4
#-*- coding:Utf8 -*
import pickle   #Permet l'ouverture des fichiers en mode binaire
"""
********************************************************************
Ce module contient toute les fonctions qui vont attribuer, effacer\
et modifier les données uilisateurs.\
Les données utilisateurs sont stockées dans un fichier binaire sous \
cette forme:
{
    user_id :{  historique:
                { mess-id: ...
                  mess-id: ...
                }
                parametres:
                { option1: ...
                  option2: ...
                }
            }
    user_id: .....
}
*******************************************************************
"""
def identification(msg,bot):
#Ouverture de la base de données, test de l'existance de l'utilisateur à l'intérieur :  Création de l'utilisateur si il n'existe pas et mise à jour de l'historique s'il existe. Puis renvoie des données utilisateur dans tous les cas
	nouveauU=True
	with open("UserData","rb") as fichier :
		monPickler = pickle.Unpickler(fichier)
		DataBank = monPickler.load()
		for i,elt in enumerate(DataBank):
			if DataBank[i]['user_id']==msg['from']['id']:
				nouveauU = False            #nouveauU = False si l'utilisateur existe déjà
				DataBank[i]['historique'][msg['message_id']]=msg
				#Ajout du message recu dans l'historique utilisateur
				print('Reception d\'un message de',msg['from']['last_name'])
				#print(DataBank)
				DonneesUtilisateur = DataBank[i]
		if nouveauU == True :
			Data={'user_id':msg['from']['id'],'historique':{msg['message_id']: msg},'parametres':{}}
			DataBank.append(Data)
			print("Ajout d'un nouvel utilisateur, last_name= ",msg['from']['last_name'])
			DonneesUtilisateur = DataBank[0]
			i=len(DataBank)-1
#Cette partie reste à optimiser lorsque l'on sera plus sur de ce qu'on va retenir de
#chaque utilisateur et de ce que l'on a comme paramètres sur chacun d'entre eux

#Ces données sont renvoyées pour être réutilisées dans le main
		

#On fait une mise à jour de la base
	with open("UserData","wb") as fichier:
		monPickler = pickle.Pickler(fichier)
		monPickler.dump(DataBank)
	return(nouveauU,i,DonneesUtilisateur)


