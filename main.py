import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


data = []
timeday = time.strftime("%d-%m-%Y")

cookies = {'session': 'Your_log_cookie'}
webhook_url = 'Discord_Webhook'

categorie = input("Entrez le numéro de la catégorie que vous voulez extraire : \n 1. Full Applications \n 2. Plugins \n 3. Tutorials \n 4. Models \n 5. Materials \n 6. Misc \n 7. GameDev \n 8. Par Nom\n")

if int(categorie)<8:
    page = 0
    while True:
        page += 1
        url = 'https://cgpeers.to/torrents.php?page='+ str(page) +'&searchstr=&order_by=time&order_way=desc&filter_cat%5B'+ str(categorie) +'%5D=1&searchsubmit=1'
        response = requests.get(url, cookies=cookies)
        soup = BeautifulSoup(response.content, 'html.parser')
        torrents = soup.find_all('tr', class_='torrent')


        if soup.find('h2', text='The requested page contains no matches.'):
            break

        for torrent in torrents:
            title = torrent.find('a', title='View Torrent')
            if title:
                name = title.text
                download_link = torrent.find('a', title='Download')
                if download_link:
                    download_url = download_link['href']
                    data.append({
                        'Name': name,
                        'Download Link': "https://cgpeers.to/" + download_url
                        })


    df = pd.DataFrame(data)




    if categorie == "1":
        categoriename = "Full Applications"
    elif categorie == "2":
        categoriename = "Plugins"
    elif categorie == "3":
        categoriename = "Tutorials"
    elif categorie == "4":
        categoriename = "Models"
    elif categorie == "5":
        categoriename = "Materials"
    elif categorie == "6":
        categoriename = "Misc"
    elif categorie == "7":
        categoriename = "GameDev"






    df.to_excel(str(categoriename)+ str(timeday) +'.xlsx', index=False)
    print (categoriename +' Done!')

    senddiscord = input("Voulez-vous envoyer le fichier sur discord ? (y/n) : ")

    if senddiscord == "y" or senddiscord == "Y":
        response = requests.post(files={'file': open(str(categoriename)+ str(timeday) +'.xlsx', 'rb')}, url=webhook_url)
    elif senddiscord == "n" or senddiscord == "N":
        print("Ok, bye !")
    else:
        print("Erreur, bye !")
        
        
        
elif int(categorie) == 8:
    Name = input("Entrez le nom des torrent que vous voulez extraire : ")
    form_data = {
        'searchstr' : Name,
    }
    page = 0
    found_results = False
    
    while True:
        page += 1
        url = f'https://cgpeers.to/torrents.php?page={page}&searchstr={Name}&order_by=time&order_way=desc&searchsubmit=1'
        response = requests.get(url, cookies=cookies)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        torrents = soup.find_all('tr', class_='torrent')

        # Vérifier si la page contient des données
        if soup.find('h2', text='The requested page contains no matches.'):
            break
        
        # Ajouter les noms et les liens de téléchargement à la liste
        for torrent in torrents:
            title = torrent.find('a', title='View Torrent')
            if title:
                found_results = True
                name = title.text
                download_link = torrent.find('a', title='Download')
                if download_link:
                    download_url = download_link['href']
                    data.append({
                        'Name': name,
                        'Download Link': "https://cgpeers.to/" + download_url
                        })

    if not found_results: # check if no results were found
        print("Aucun résultat trouvé")
    else:
        # Créer un DataFrame de pandas à partir de la liste de données
        df = pd.DataFrame(data)
        df.to_excel(Name+ str(timeday) +'.xlsx', index=False)
        print (Name +' Done!')


