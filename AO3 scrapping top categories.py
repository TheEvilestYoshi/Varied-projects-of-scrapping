import pdb
import re
import requests
import json
import datetime
import time

req_get_header = {'User_agent':"(Mozilla/5.0(Windows; U;WindowsNT6.0\;en-us;rv:1.9.2)Gecko/20100115 Firefox/3.6"}
dossier_sauvegarde ="C:/Users/Acer/Desktop/M1 SDIN-S2/python/"

#this scripts scraps datas from the fanfiction website AO3 also known as Archive of Our Own.
#its aim was to provide analytics on the factors of success of fanfictions related to their numbers of readers, likes, contents and tag system
# it can be combined with the "AO3 wiki" that pulls data from the wikipedia API to give further informations
#all stories belong to their authors
#Reminder that this project was done for academical purpose and no commercial use can be done of those informations.
urlStarWars ='https://archiveofourown.org/tags/Star%20Wars%20-%20All%20Media%20Types/works?page='
urlHarryPotter = 'https://archiveofourown.org/tags/Harry%20Potter%20-%20J*d*%20K*d*%20Rowling/works?page='
urlSherlock='https://archiveofourown.org/tags/Sherlock%20Holmes%20*a*%20Related%20Fandoms/works?page='
urlTolkien ='https://archiveofourown.org/tags/TOLKIEN%20J*d*%20R*d*%20R*d*%20-%20Works%20*a*%20Related%20Fandoms/works?page='
urlDragonAge ='https://archiveofourown.org/tags/Dragon%20Age%20-%20All%20Media%20Types/works?page='
LFD ={"Star Wars":urlStarWars}
LFD2 ={"Star Wars":urlStarWars,"Harry Potter":urlHarryPotter,"Sherlock Holmes":urlSherlock,"Tolkien":urlTolkien,"Dragon Age":urlDragonAge} # dictionnaire de bouclage
#NOTES SYSTEME/DEV/TODO

#que la première fois
BASE1 = {"AO3":{}}

#ouverture du dictionnaire pour la méthode multipassage
for FD in LFD:
    ultimate_decount = 10 #positionneur de page, on réfléchi en sens inverse pour éviter le problème des déplacement de chargement, si par malheur une fanfic etait mise à jour, cela fausserait la collecte de données donc on réfléchit en arrière pour éviter les doublons
    while ultimate_decount > 7: #numero de page ou on s'arrête
        urlcomb = str(LFD[FD]) + str(ultimate_decount) #url combinée des 2 morceaux
        req = requests.get(urlcomb,headers=req_get_header,timeout = 60)
        content =req.text
        print(urlcomb)
        #sauvegarde format texte de la page
        """
        with open(dossier_sauvegarde +"first.txt","w",encoding ='utf-8') as outfile:
            outfile.write(content)
        """
        date = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S') #reset de date pour contourner le souci de doublons jusqu'a ce que le detecteur soit ok
        LENTEXTE = len(content)
        Test = 0
        ListePosition = [] #liste ressortant l'ensemble des positions des fanfics par page, penser, à boucler par page
        while Test != -1:
            Test = content.find('<!--title, author, fandom-->\n  <div class="header module">\n\n    <h4 class="heading">',Test +1)
            ListePosition.append(Test)

        ListePosition[len(ListePosition) - 1]=LENTEXTE #permet la cloture en remplaçant le -1 final
        LenListe=len(ListePosition)

        #on a la liste de tous les positionnement de texte, on peut maintenant aller chercher les données

        # TO DO : éliminer le risque des dédoublements, corriger le CSV, exporter le CSV, récupérer les données des items croisés

        boucleur1= 0
        POS1 = 0 #position d'entrée de recherce
        POS2 = 0 #position de sortie de recherche

        LenListeCor = LenListe - 1  # longueur liste corrigée pour que la boucle for accepte
        while boucleur1 != LenListeCor:
            POS1 = ListePosition[boucleur1]
            POS2 = ListePosition[boucleur1 + 1] #permet de se mettre au bout du texte quand LenListe - 1 = max)

            patternTitre ='<h4 class="heading">\n      <a href=(.{1,150})</a>\n      by'
            TitreRAW = re.findall(patternTitre,content[POS1:POS2]) #necessite un nettoyage, on ne garde pas l'ID WORK
            Titredebut = TitreRAW[0].find('">') #trouve le début du titre en valeur numérique
            Titrefin = len(TitreRAW[0])
            TitreCLEAN = TitreRAW[0][Titredebut + 2:Titrefin] #+2 car "> fait 2 caractères
            
            boucleur1 = boucleur1 +1 # on avance dans les section, doit se trouver en fin des if et else si construit comme tel
            #checker que le TitreCLEAN existe pour éviter l'overwrite
            #PRIORITE 1
            BASE1['AO3'][TitreCLEAN]={}
            BASE1['AO3'][TitreCLEAN][date] ={} #on doit rentrer les dictionnaires 1 par 1

            auteurpattern ='<a rel="author" href="/users/(.{1,36})/pseuds/'
            Aut = re.findall(auteurpattern,content[POS1:POS2])
            BASE1['AO3'][TitreCLEAN][date]['Auteur/Autrice']=Aut

            #ajout de source universe
            BASE1['AO3'][TitreCLEAN][date]['UnivSource']=str(FD)
            #### revoir les fandom tags

            opener = content.find('<h5 class="fandoms heading"',POS1)
            closer = content.find('</h5>',opener) #reprend l'ouverture pour être en suite
            zonetravail =content[opener:closer] #zone de travail ou on a les tags pour éviter les faux positifs et les problèmes de fermeture
            patterntagfandomraw = '<a class="tag" href="/tags/(.{1,100})</a>'
            tagfandomraw = re.findall(patterntagfandomraw,content[opener:closer])
            tagfandomclean =[]
            for item in tagfandomraw:
                positionfandomtag = item.find('">')
                temp0 = item[positionfandomtag +2:]
                tagfandomclean.append(temp0)

            BASE1['AO3'][TitreCLEAN][date]['Fandom']=tagfandomclean
            
            ###fin révision fandom tags avec DROUARD
            
            WarTagpattern ='<li class=\\\'warnings\\\'><strong><a class="tag" href="(.{1,140})</a></strong>'
            Warnings =re.findall(WarTagpattern,content[POS1:POS2])
            WarnTagClean =[]
            for item in Warnings:
                positionwartagdelimitor = item.find('">') #chercher dans l'item qui est dans le warning
                temp1 = item[positionwartagdelimitor + 2:]
                WarnTagClean.append(temp1) #version clean

            BASE1['AO3'][TitreCLEAN][date]['Warnings']=WarnTagClean #ajout au dico

            WarningImagepattern ='<a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class=(.+?(?=</span></span></a></li>))'
            # corrigé avec la méthode
            WarimageRaw = re.findall(WarningImagepattern, content[POS1:POS2])
            WarimageClean =[]
            for item in WarimageRaw:
                warimagedelimator =item.find('<span class="text">') 
                tempW=item[warimagedelimator + 19:]
                WarimageClean.append(tempW)
            BASE1['AO3'][TitreCLEAN][date]['WarningImages']=WarimageClean 
            
            Relpattern ='<li class=\\\'relationships\\\'><a class="tag" href="/tags/(.{1,90})</a></li>' #usage d'échappes
            RelTag = re.findall(Relpattern,content[POS1:POS2]) #doit être nettoyé avec le ">
            RelTagclean = []
            for item in RelTag:
                positionreltagdelimitor = item.find('">')
                temp2 = item[positionreltagdelimitor + 2:]
                RelTagclean.append(temp2) #version nettoyée en format liste
                # problème séparateur runaround sur la taille des RE mais voir avoir DROUARD ou JACQ

            BASE1['AO3'][TitreCLEAN][date]['Relations']=RelTagclean
            
            Charpattern ='<li class=\\\'characters\\\'><a class="tag" href="/tags/(.+?(?=</a></li>))'
            Character = re.findall(Charpattern,content[POS1:POS2])
            Charpatternclean=[] #création/Reset
            for item in Character:
                positionchardelimitor = item.find('">')
                temp3 = item[positionchardelimitor +2:]
                Charpatternclean.append(temp3)

            BASE1['AO3'][TitreCLEAN][date]['Personnages']=Charpatternclean
            
            #problème de séparation des tags, CORRIGE
            FreeformPattern='<li class=\\\'freeforms\\\'><a class="tag" href="/tags/(.+?(?=</a></li>))'
            Freeform = re.findall(FreeformPattern, content[POS1:POS2])
            Freeformclean =[] #création/Reset
            for item in Freeform:
                positionfreedelimitor = item.find('">')
                temp4 = item[positionfreedelimitor+2:]
                Freeformclean.append(temp4)
            
            BASE1['AO3'][TitreCLEAN][date]['FreeformTags']=Freeformclean

            Languagepattern ='<dd class="language">(.{1,18})</dd>'
            langage = re.findall(Languagepattern,content[POS1:POS2])

        # note, pour les morceaux à venir même si ils existent pas, on prend et on range
            BASE1['AO3'][TitreCLEAN][date]['Langue']=langage

            wordcountpattern ='<dd class="words">(.{1,9})</dd>'
            wordcount = re.findall(wordcountpattern,content[POS1:POS2])

            BASE1['AO3'][TitreCLEAN][date]['WordCount']=wordcount

            chapterspattern ='<dd class="chapters">(.{1,4})</dd>'
            chapters = re.findall(chapterspattern,content[POS1:POS2])
            if len(chapters) == 0: #vérifier existence de la base ou rentre la valeur défaut
                BASE1['AO3'][TitreCLEAN][date]['Chapitre']= 1
            else:
                BASE1['AO3'][TitreCLEAN][date]['Chapitre']=chapters
            
            kudospattern ='<dd class="kudos">(.{1,100})</a></dd>'
            kudos =re.findall(kudospattern,content[POS1:POS2])#nécessité un nettoyage
            kudosclean =[]
            if len(kudos)==0: #repeat de vérif de l'existence
                BASE1['AO3'][TitreCLEAN][date]['Kudos']=0    
            else:
                for item in kudos:
                    positionkudosdelimitor= item.find('">')
                    temp5 = item[positionkudosdelimitor+2:]
                    kudosclean.append(temp5)
            
                BASE1['AO3'][TitreCLEAN][date]['Kudos']=kudosclean    
                             
            resumepattern ='Summary</h6>\n    <blockquote class="userstuff summary">\n      <p>(.{1,1250})\n    </blockquote>\n'
            Lresume = re.findall(resumepattern,content[POS1:POS2]) #penser à flaguer

            BASE1['AO3'][TitreCLEAN][date]['Résumé']=Lresume

            bookmarkpattern ='<dd class="bookmarks"><a href="(.{1,70})</a></dd>'
            Lbookmarkraw = re.findall(bookmarkpattern,content[POS1:POS2]) # nécessite néttoyage
            Lbookmarkclean=[] #clear/reset
            if len(Lbookmarkraw) ==0:
                BASE1['AO3'][TitreCLEAN][date]['Bookmarks']=0
            else:
                for item in Lbookmarkraw:
                    positionbookmarkdelimitor=item.find('">')
                    temp6 = item[positionbookmarkdelimitor+2:]
                    Lbookmarkclean.append(temp6)
                
                BASE1['AO3'][TitreCLEAN][date]['Bookmarks']=Lbookmarkclean
            
            hitspattern ='<dt class="hits">Hits:</dt>\n    <dd class="hits">(.+?(?=</dd>))' #ça marche comme ça pour le moment, on pose pas de questions !
            hitsfind = re.findall(hitspattern,content[POS1:POS2])
            if len(hitsfind) ==0: #clear des 0, on vérifie que notre liste et nulle
                BASE1['AO3'][TitreCLEAN][date]['Hits'] = 0
            else:
                BASE1['AO3'][TitreCLEAN][date]['Hits'] = hitsfind

        ultimate_decount = ultimate_decount - 1 # bien désaxer de 1 incrément, on change la page, pas l'article

Bourne = BASE1
with open(dossier_sauvegarde+"dicoSw60dec.json","w") as output:
    json.dump(Bourne,output) #j'aime trop cette blague pour l'abandonner


# sortir en CSV

