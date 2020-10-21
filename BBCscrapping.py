import pdb
import re
import requests
import json
import datetime

#Study notes :
# code could be optimized if a dictionnary was used for the patterns
# needs a created save file beforehand preloaded or use the "BASE in line 38"
#reminder that all those programs are done for academical purpose and all datas must be destroyed after use.

req_get_header = {'User_agent':"(Mozilla/5.0(Windows; U;WindowsNT6.0\;en-us;rv:1.9.2)Gecko/20100115 Firefox/3.6"}
dossier_sauvegarde ="C:/Users/Acer/Desktop/M1 SDIN/python/projetpython/sauvegardeBBC"
url_entree_BBC ="https://www.bbc.co.uk/news/world"

req = requests.get(url_entree_BBC,headers=req_get_header,timeout = 60)
content =req.text
date = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M')
print(date)

with open(dossier_sauvegarde +"/BBCoriginal.txt","w",encoding ='utf-8') as outfile:
    outfile.write(content)

# un pattern par region du monde, mais il se peut que plusieurs balises répondent à l'appel

pattern_ME ='/news/world-middle-east-(.{1,15})">'
pattern_USACAN ='/news/world-us-canada-(.{1,15})">'
pattern_ASIA ='/news/world-asia-(.{1,15})">'
pattern_LATAM ='/news/world-latin-america-(.{1,15})">'
pattern_EU='/news/world-europe-(.{1,15})">' 
pattern_AUS='/news/world-australia-(.{1,15})">'
pattern_AF='/news/world-africa-(.{1,15})">'

#création d'une liste pour les patterns dont on se servira par la suite
listepatt=[pattern_ME,pattern_USACAN,pattern_ASIA,pattern_LATAM,pattern_EU,pattern_AUS,pattern_AF]

#construction d'un dictionnaire par region et d'une liste regroupant tous les articles
"""
Base = {"Codes_Pages":{"Changelog":{},"Liste":[],"Quantité":0},"Categories":{"ME" :{"Quantité":0,"Changelog":{},"Liste":[],"Articles":{}},"USACAN" :{"Quantité":0,"Changelog":{},"Liste":[],"Articles":{}},"ASIA":{"Quantité":0,"Changelog":{},"Liste":[],"Articles":{}},"LATAM":{"Quantité":0,"Changelog":{},"Liste":[],"Articles":{}},"EU":{"Quantité":0,"Changelog":{},"Liste":[],"Articles":{}},"AUS":{"Quantité":0,"Changelog":{},"Liste":[],"Articles":{}},"AF":{"Quantité":0,"Changelog":{},"Liste":[],"Articles":{}}}}
"""
# ouverture du dictionnaire qu'on a construit les fois précédentes

with open('C:/Users/Acer/Desktop/M1 SDIN/python/projetpython/sauvegardeBBC/dico.json',"r") as infile:
        Base=json.load(infile)

# on part à la chasse aux articles, on commence par le ME et on généralise la méthode, pas de liste car pas de succès

################ ME
results = re.findall(pattern_ME,content)
listeajouts=[]
for item in results:
    if item not in Base["Categories"]["ME"]["Liste"]: # on vérifie qu'on ne connait pas l'article
        Base["Categories"]["ME"]["Liste"].append(item) # l'ajoute à la liste des connus
        Base["Categories"]["ME"]["Articles"][item]={} # l'ajoute à la liste des articles en tant que dico pour ajouter ses données dans le futur
        ### faire la recherche des systèmes dedans
        internal_request= requests.get(url_entree_BBC+'-middle-east-'+item,headers=req_get_header,timeout = 20)
        internal_content = internal_request.text
        
        with open(dossier_sauvegarde +"/"+item+".txt","w",encoding ='utf-8') as outfile:
            outfile.write(internal_content)#sauvegarde du dossier

        art_titre = re.findall('<h1 class="story-body__h1">(.{1,200})</h1>\n',internal_content) # titre de l'article
        liste_tag = []
        art_tag = re.findall('<a href="/news/topics/c(.{1,100})</a>',internal_content)
        for tag in art_tag:        
            a1=tag.find('">') # on nettoie la "crasse" de la recherche en récupérant le début du mot clé voulu
            lentag = len(tag)
            truetag = tag[a1+2:lentag]
            if truetag not in liste_tag: #(on ajoute le vrai tag à la liste)
                liste_tag.append(truetag)
            else:
                1 #do nothing and move on
        
        Base["Categories"]["ME"]["Articles"][item]['Date']=date # on donne la date
        Base["Categories"]["ME"]["Articles"][item]['Tag'] = liste_tag # on met ses tags
        Base["Categories"]["ME"]["Articles"][item]['Titre'] = art_titre # on met son titre
        listeajouts.append(item)
    else:
        1 #do nothing
Base["Categories"]["ME"]["Changelog"][date]=listeajouts # met à jour le changelog avec la date
Base["Categories"]["ME"]["Quantité"] = Base["Categories"]["ME"]["Quantité"] + len(listeajouts) # met à jour le nombre d'articles

# on crée la date dans le changelog UNE SEULE FOIS pour le générique
Base["Codes_Pages"]["Changelog"][date]=[]
for ajouts in listeajouts:
    Base["Codes_Pages"]["Liste"].append('/news/world-middle-east-'+ajouts) # ajout dans la liste générique
    Base["Codes_Pages"]["Changelog"][date].append('/news/world-middle-east-'+ajouts) #ajout dans la liste changelog    
Base["Codes_Pages"]["Quantité"]=Base["Codes_Pages"]["Quantité"] + len(listeajouts)

listeajouts = [] # reset de la liste, on peut passer à l'ensemble suivant et juste changer les noms à défaut d'utiliser un dictionnaire

################## USA CAN - OK

results = re.findall(pattern_USACAN,content)
listeajouts=[]
for item in results:
    if item not in Base["Categories"]["USACAN"]["Liste"]:
        Base["Categories"]["USACAN"]["Liste"].append(item) # l'ajoute à la liste des connus
        Base["Categories"]["USACAN"]["Articles"][item]={} # l'ajoute à la liste des articles en tant que dico pour ajouter ses données dans le futur
        internal_request= requests.get(url_entree_BBC+'-us-canada-'+item,headers=req_get_header,timeout = 20)
        internal_content = internal_request.text
        
        with open(dossier_sauvegarde +"/"+item+".txt","w",encoding ='utf-8') as outfile:
            outfile.write(internal_content)#sauvegarde du dossier

        art_titre = re.findall('<h1 class="story-body__h1">(.{1,200})</h1>\n',internal_content) # titre de l'article
        liste_tag = []
        art_tag = re.findall('<a href="/news/topics/c(.{1,100})</a>',internal_content)
        for tag in art_tag:        
            a1=tag.find('">') # on nettoie la "crasse" de la recherche en récupérant le début du mot clé voulu
            lentag = len(tag)
            truetag = tag[a1+2:lentag]
            if truetag not in liste_tag: #(on ajoute le vrai tag à la liste)
                liste_tag.append(truetag)
            else:
                1 #do nothing and move on
        
        Base["Categories"]["USACAN"]["Articles"][item]['Date']=date # on donne la date
        Base["Categories"]["USACAN"]["Articles"][item]['Tag'] = liste_tag # on met ses tags
        Base["Categories"]["USACAN"]["Articles"][item]['Titre'] = art_titre # on met son titre
        listeajouts.append(item)
    else:
        1 #do nothing

Base["Categories"]["USACAN"]["Changelog"][date]=listeajouts # met à jour le changelog avec la date
Base["Categories"]["USACAN"]["Quantité"] = Base["Categories"]["USACAN"]["Quantité"] + len(listeajouts) # met à jour le nombre d'articles


for ajouts in listeajouts:
    Base["Codes_Pages"]["Liste"].append('/news/world-us-canada-'+ajouts) # ajout dans la liste générique
    Base["Codes_Pages"]["Changelog"][date].append('/news/world-us-canada-'+ajouts) #ajout dans la liste changelog    
Base["Codes_Pages"]["Quantité"]=Base["Codes_Pages"]["Quantité"] + len(listeajouts)

################## ASIA

results = re.findall(pattern_ASIA,content)
listeajouts=[]
for item in results:
    if item not in Base["Categories"]["ASIA"]["Liste"]:
        Base["Categories"]["ASIA"]["Liste"].append(item) # l'ajoute à la liste des connus
        Base["Categories"]["ASIA"]["Articles"][item]={} # l'ajoute à la liste des articles en tant que dico pour ajouter ses données dans le futur
        internal_request= requests.get(url_entree_BBC+'-asia-china-'+item,headers=req_get_header,timeout = 20)
        internal_content = internal_request.text
        
        with open(dossier_sauvegarde +"/"+item+".txt","w",encoding ='utf-8') as outfile:
            outfile.write(internal_content)#sauvegarde du dossier

        art_titre = re.findall('<h1 class="story-body__h1">(.{1,200})</h1>\n',internal_content) # titre de l'article
        liste_tag = []
        art_tag = re.findall('<a href="/news/topics/c(.{1,100})</a>',internal_content)
        for tag in art_tag:        
            a1=tag.find('">') # on nettoie la "crasse" de la recherche en récupérant le début du mot clé voulu
            lentag = len(tag)
            truetag = tag[a1+2:lentag]
            if truetag not in liste_tag: #(on ajoute le vrai tag à la liste)
                liste_tag.append(truetag)
            else:
                1 #do nothing and move on
        
        Base["Categories"]["ASIA"]["Articles"][item]['Date']=date # on donne la date
        Base["Categories"]["ASIA"]["Articles"][item]['Tag'] = liste_tag # on met ses tags
        Base["Categories"]["ASIA"]["Articles"][item]['Titre'] = art_titre # on met son titre
        listeajouts.append(item)
    else:
        1 #do nothing

Base["Categories"]["ASIA"]["Changelog"][date]=listeajouts # met à jour le changelog avec la date
Base["Categories"]["ASIA"]["Quantité"] = Base["Categories"]["ASIA"]["Quantité"] + len(listeajouts) # met à jour le nombre d'articles


for ajouts in listeajouts:
    Base["Codes_Pages"]["Liste"].append('/news/world-asia-china-'+ajouts) # ajout dans la liste générique
    Base["Codes_Pages"]["Changelog"][date].append('/news/world-asia-'+ajouts) #ajout dans la liste changelog    
Base["Codes_Pages"]["Quantité"]=Base["Codes_Pages"]["Quantité"] + len(listeajouts)

################## LATAM

results = re.findall(pattern_LATAM,content)
listeajouts=[]
for item in results:
    if item not in Base["Categories"]["LATAM"]["Liste"]:
        Base["Categories"]["LATAM"]["Liste"].append(item) # l'ajoute à la liste des connus
        Base["Categories"]["LATAM"]["Articles"][item]={} # l'ajoute à la liste des articles en tant que dico pour ajouter ses données dans le futur
        internal_request= requests.get(url_entree_BBC+'-latin-america-'+item,headers=req_get_header,timeout = 20)
        internal_content = internal_request.text
        
        with open(dossier_sauvegarde +"/"+item+".txt","w",encoding ='utf-8') as outfile:
            outfile.write(internal_content)#sauvegarde du dossier

        art_titre = re.findall('<h1 class="story-body__h1">(.{1,200})</h1>\n',internal_content) # titre de l'article
        liste_tag = []
        art_tag = re.findall('<a href="/news/topics/c(.{1,100})</a>',internal_content)
        for tag in art_tag:        
            a1=tag.find('">') # on nettoie la "crasse" de la recherche en récupérant le début du mot clé voulu
            lentag = len(tag)
            truetag = tag[a1+2:lentag]
            if truetag not in liste_tag: #(on ajoute le vrai tag à la liste)
                liste_tag.append(truetag)
            else:
                1 #do nothing and move on
        
        Base["Categories"]["LATAM"]["Articles"][item]['Date']=date # on donne la date
        Base["Categories"]["LATAM"]["Articles"][item]['Tag'] = liste_tag # on met ses tags
        Base["Categories"]["LATAM"]["Articles"][item]['Titre'] = art_titre # on met son titre
        listeajouts.append(item)
    else:
        1 #do nothing

Base["Categories"]["LATAM"]["Changelog"][date]=listeajouts # met à jour le changelog avec la date
Base["Categories"]["LATAM"]["Quantité"] = Base["Categories"]["LATAM"]["Quantité"] + len(listeajouts) # met à jour le nombre d'articles


for ajouts in listeajouts:
    Base["Codes_Pages"]["Liste"].append('/news/world-latin-america-'+ajouts) # ajout dans la liste générique
    Base["Codes_Pages"]["Changelog"][date].append('/news/world-latin-america-'+ajouts) #ajout dans la liste changelog    
Base["Codes_Pages"]["Quantité"]=Base["Codes_Pages"]["Quantité"] + len(listeajouts)

################## EU

results = re.findall(pattern_EU,content)
listeajouts=[]
for item in results:
    if item not in Base["Categories"]["EU"]["Liste"]:
        Base["Categories"]["EU"]["Liste"].append(item) # l'ajoute à la liste des connus
        Base["Categories"]["EU"]["Articles"][item]={} # l'ajoute à la liste des articles en tant que dico pour ajouter ses données dans le futur
        internal_request= requests.get(url_entree_BBC+'-europe-'+item,headers=req_get_header,timeout = 20)
        internal_content = internal_request.text
        
        with open(dossier_sauvegarde +"/"+item+".txt","w",encoding ='utf-8') as outfile:
            outfile.write(internal_content)#sauvegarde du dossier

        art_titre = re.findall('<h1 class="story-body__h1">(.{1,200})</h1>\n',internal_content) # titre de l'article
        liste_tag = []
        art_tag = re.findall('<a href="/news/topics/c(.{1,100})</a>',internal_content)
        for tag in art_tag:        
            a1=tag.find('">') # on nettoie la "crasse" de la recherche en récupérant le début du mot clé voulu
            lentag = len(tag)
            truetag = tag[a1+2:lentag]
            if truetag not in liste_tag: #(on ajoute le vrai tag à la liste)
                liste_tag.append(truetag)
            else:
                1 #do nothing and move on
        Base["Categories"]["EU"]["Articles"][item]['Date']=date # on donne la date
        Base["Categories"]["EU"]["Articles"][item]['Tag'] = liste_tag # on met ses tags
        Base["Categories"]["EU"]["Articles"][item]['Titre'] = art_titre # on met son titre
        listeajouts.append(item)
    else:
        1 #do nothing
  
Base["Categories"]["EU"]["Changelog"][date]=listeajouts # met à jour le changelog avec la date
Base["Categories"]["EU"]["Quantité"] = Base["Categories"]["EU"]["Quantité"] + len(listeajouts) # met à jour le nombre d'articles


for ajouts in listeajouts:
    Base["Codes_Pages"]["Liste"].append('/news/world-europe-'+ajouts) # ajout dans la liste générique
    Base["Codes_Pages"]["Changelog"][date].append('/news/world-europe-'+ajouts) #ajout dans la liste changelog    
Base["Codes_Pages"]["Quantité"]=Base["Codes_Pages"]["Quantité"] + len(listeajouts)

################## AUS

results = re.findall(pattern_AUS,content)
listeajouts=[]
for item in results:
    if item not in Base["Categories"]["AUS"]["Liste"]:
        Base["Categories"]["AUS"]["Liste"].append(item) # l'ajoute à la liste des connus
        Base["Categories"]["AUS"]["Articles"][item]={} # l'ajoute à la liste des articles en tant que dico pour ajouter ses données dans le futur
        internal_request= requests.get(url_entree_BBC+'-australia-'+item,headers=req_get_header,timeout = 20)
        internal_content = internal_request.text
        
        with open(dossier_sauvegarde +"/"+item+".txt","w",encoding ='utf-8') as outfile:
            outfile.write(internal_content)#sauvegarde du dossier

        art_titre = re.findall('<h1 class="story-body__h1">(.{1,200})</h1>\n',internal_content) # titre de l'article
        liste_tag = []
        art_tag = re.findall('<a href="/news/topics/c(.{1,100})</a>',internal_content)
        for tag in art_tag:        
            a1=tag.find('">') # on nettoie la "crasse" de la recherche en récupérant le début du mot clé voulu
            lentag = len(tag)
            truetag = tag[a1+2:lentag]
            if truetag not in liste_tag: #(on ajoute le vrai tag à la liste)
                liste_tag.append(truetag)
            else:
                1 #do nothing and move on
        Base["Categories"]["AUS"]["Articles"][item]['Date']=date # on donne la date
        Base["Categories"]["AUS"]["Articles"][item]['Tag'] = liste_tag # on met ses tags
        Base["Categories"]["AUS"]["Articles"][item]['Titre'] = art_titre # on met son titre
        listeajouts.append(item)
    else:
        1 #do nothing

Base["Categories"]["AUS"]["Changelog"][date]=listeajouts # met à jour le changelog avec la date
Base["Categories"]["AUS"]["Quantité"] = Base["Categories"]["AUS"]["Quantité"] + len(listeajouts) # met à jour le nombre d'articles


for ajouts in listeajouts:
    Base["Codes_Pages"]["Liste"].append('/news/world-australia-'+ajouts) # ajout dans la liste générique
    Base["Codes_Pages"]["Changelog"][date].append('/news/world-australia-'+ajouts) #ajout dans la liste changelog    
Base["Codes_Pages"]["Quantité"]=Base["Codes_Pages"]["Quantité"] + len(listeajouts)

################## AF

results = re.findall(pattern_AF,content)
listeajouts=[]
for item in results:
    if item not in Base["Categories"]["AF"]["Liste"]:
        Base["Categories"]["AF"]["Liste"].append(item) # l'ajoute à la liste des connus
        Base["Categories"]["AF"]["Articles"][item]={} # l'ajoute à la liste des articles en tant que dico pour ajouter ses données dans le futur
        internal_request= requests.get(url_entree_BBC+'-africa-'+item,headers=req_get_header,timeout = 20)
        internal_content = internal_request.text
        
        with open(dossier_sauvegarde +"/"+item+".txt","w",encoding ='utf-8') as outfile:
            outfile.write(internal_content)#sauvegarde du dossier

        art_titre = re.findall('<h1 class="story-body__h1">(.{1,200})</h1>\n',internal_content) # titre de l'article
        liste_tag = []
        art_tag = re.findall('<a href="/news/topics/c(.{1,100})</a>',internal_content)
        for tag in art_tag:        
            a1=tag.find('">') # on nettoie la "crasse" de la recherche en récupérant le début du mot clé voulu
            lentag = len(tag)
            truetag = tag[a1+2:lentag]
            if truetag not in liste_tag: #(on ajoute le vrai tag à la liste)
                liste_tag.append(truetag)
            else:
                1 #do nothing and move on
        Base["Categories"]["AF"]["Articles"][item]['Date']=date # on donne la date
        Base["Categories"]["AF"]["Articles"][item]['Tag'] = liste_tag # on met ses tags
        Base["Categories"]["AF"]["Articles"][item]['Titre'] = art_titre # on met son titre
        listeajouts.append(item)
    else:
        1 #do nothing

Base["Categories"]["AF"]["Changelog"][date]=listeajouts # met à jour le changelog avec la date
Base["Categories"]["AF"]["Quantité"] = Base["Categories"]["AF"]["Quantité"] + len(listeajouts) # met à jour le nombre d'articles


for ajouts in listeajouts:
    Base["Codes_Pages"]["Liste"].append('/news/world-africa-'+ajouts) # ajout dans la liste générique
    Base["Codes_Pages"]["Changelog"][date].append('/news/world-africa-'+ajouts) #ajout dans la liste changelog    
Base["Codes_Pages"]["Quantité"]=Base["Codes_Pages"]["Quantité"] + len(listeajouts)


# sauvegarde en json Bourne
Bourne = Base
with open(dossier_sauvegarde +"/dico.json","w") as output:
    json.dump(Bourne,output)

