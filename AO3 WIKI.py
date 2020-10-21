
import pdb
import re
import requests
import json
import datetime
import csv
import time
import wptools

req_get_header = {'User_agent':"(Mozilla/5.0(Windows; U;WindowsNT6.0\;en-us;rv:1.9.2)Gecko/20100115 Firefox/3.6"}
dossier_sauvegarde ="C:/Users/Acer/Desktop/M1 SDIN-S2/python/"

#you can open any dictionnary or json made out of the database of characters from the previous script
with open('C:/Users/Acer/Desktop/M1 SDIN-S2/python/dicoSw60dec.json',"r") as infile:
        BASE1=json.load(infile)
#pour la démonstration on bosse sur la base harry Potter 100 nouvelles

BASE1["Personnages"]={}
BASE1["Personnages"]["Connus"]={}
BASE1["Personnages"]["Connus"]['Liste']=[]
BASE1["Personnages"]["Non reconnus"]={}
BASE1["Personnages"]["Non reconnus"]['Liste']=[]
#on construit la nouvelle branche de la base
# on va maintenant chercher tous les personnages de toutes les fanfictions
for item in BASE1['AO3'].keys():
    for itemdate in BASE1['AO3'][item].keys():
        for itempersonnage in BASE1['AO3'][item][itemdate]["Personnages"]: # on est arrivé aux personnages et c'est une liste
            if itempersonnage not in BASE1['Personnages']['Non reconnus']['Liste']:
                if itempersonnage not in BASE1["Personnages"]["Connus"]['Liste']:
                    try:
                        paste =wptools.page(itempersonnage,lang='fr').get_parse()
                        # on va test et try tous les éléments qu'on désire avoir, seule façon qu'on a de tout compiler
                        BASE1["Personnages"]["Connus"][itempersonnage]={} #création de l'entrée personnage

                        try: #ecriture taille, sauf exception il en a qu'une
                            taille = paste.infobox['taille']
                            taille = taille.replace('{',"")
                            taille = taille.replace("}","") #on nettoie la taille avant de ranger
                            taille= taille.replace("|","")
                            taile = taille.replace("unité","")
                            BASE1["Personnages"]["Connus"][itempersonnage]['Taille'] = taille
                        except:
                            1 #do nothing taille pas trouvée

                        try: #ecriture espèce
                            espèce = paste.infobox['espèce']
                            if espèce.find(']]') != -1 and espèce.find('|') != -1: # on regarde le type de stockage de l'info
                                wordingespece = espèce.find('|')
                                espèce =espèce[wordingespece+1:]
                                espèce = espèce.replace(']','')
                                BASE1["Personnages"]["Connus"][itempersonnage]['Espèce']=espèce
                            else:#stockage normal
                                BASE1["Personnages"]["Connus"][itempersonnage]['Espèce']=espèce
                        except:
                            1 #pas trouvée

                        try: #ecriture cheveux
                            cheveux = paste.infobox['cheveux']
                            BASE1["Personnages"]["Connus"][itempersonnage]['Cheveux'] = cheveux
                        except:
                            1 #do nothing

                        try: #ecriture yeux couleur
                            yeux = paste.infobox['yeux']
                            wording = yeux.find('|') # on force le texte à se finir comme ceci |Bleus]]'qu'on nettoie par la suite, méthode avec faiblesses
                            yeux = yeux[wording +1:]
                            yeux =yeux.replace(']','') #on enlève la crasse
                            BASE1["Personnages"]["Connus"][itempersonnage]['Yeux']=yeux
                        except:
                            1 # do nothing

                        try: #activité, attention il peut y en avoir plusieurs
                            activite = paste.infobox['activité']
                            activité = activité.replace('<br>','/')
                            BASE1["Personnages"]["Connus"][itempersonnage]['Activité']=activite
                        except:
                            1#do nothing

                        '''try: #arme #exceptions etranges, voir rapport
                            arme = paste.infobox['arme']
                            BASE1["Personnages"]["Connus"][itempersonnage]['Arme'] = arme
                        except:
                            1 #do nothing
                        '''
                        BASE1["Personnages"]["Connus"]['Liste'].append(itempersonnage) #ajout à la liste des connus maintenant qu'on a récupéré la page

                    # reste du deroulé  de recherched 'infos
                    except : # la recherche ne marche pas
                        BASE1["Personnages"]["Non reconnus"]['Liste'].append(itempersonnage)
                
                else:
                    1 # do nothing, on connait déjà le personnage, on a pas besoin de le documenter
            else : #déjà connucomme INTROUVABLE et recherche ne pas pas, on perd pas de temps
                1 #do nothing
            
Bourne = BASE1
with open(dossier_sauvegarde+"dicoSw60decPERSOINCLUS.json","w") as output:
    json.dump(Bourne,output) #terrible joke, but i love it.
