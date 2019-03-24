import re
import urllib.request as urllib2
import urllib
from bs4 import BeautifulSoup
import csv
import os
import time
import json
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))


def look(links,csv):
    """Scrap link of LaVoz Clasificados

    Scraps rent links looking for price, neighborhood, street, 

    Arguments:
        links {string} -- URL of appartment
        csv {list} -- Final list of results

    Returns:
        Function -- Fills the csv with new data
    """    
    quote_page = links
    # query the website and return the html to the variable ‘page’
    page = urllib2.urlopen(quote_page)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    precio=  soup.find('h3',attrs={'class','precio-visible'}).text.strip().replace('.','').replace('$','')
    #get barrio
    barrio = ""
    for link in soup.find_all('a'):
        if link.has_attr('href') and "/category/provincias/cordoba/cordoba/" in link.attrs['href']:
            barrio =  link.get_text()
    try:
        #if (int(precio)):
        calle = soup.find(string=re.compile('Calle:')).find_next('span').text.strip()
        #try to get latitud and longitud from google maps api
        url_google_maps =( "https://maps.googleapis.com/maps/api/geocode/json?address="+ calle.replace(' ','+') + '+cordoba' +',+CA&key=AIzaSyCc55I-I05MFcRf1lzbMdIHZD9SbB3h1YI')
        
        with urllib.request.urlopen(url_google_maps) as url:
            data = json.loads(url.read().decode())
            lat = data['results'][0]['geometry']['location']['lat']
            lng = data['results'][0]['geometry']['location']['lng']
            dormitorios =soup.find(string=re.compile('ormitorios')).find_next('span').text.strip()
            print("New appartment!")
            csv.append([precio, barrio, calle, dormitorios, links, lat, lng])
    except:
        pass

def general(page,counts,csvs):

    counts = counts +1
    page = urllib2.urlopen(page)
    soup = BeautifulSoup(page, 'html.parser')

    
    CD=  soup.find('div',class_='CD').find_all('div',class_='Modelo')
    for i in CD:
        look(i.find('a').attrs['href'],csvs )
    if counts <2:
        next_page = 'http://clasificados.lavoz.com.ar' +soup.find('li',class_='pager-next').find('a').attrs['href']
        time.sleep(2)
        print("New page")
        general(next_page,counts,csvs)
        
    return csvs

csvs = []
csvs.append(["precio", "barrio", "calle", "dormitorios", "links", "lat", "lng"])




def run(quote_page):
    csvfile = dir_path + '/deptos.csv'
    out= general(quote_page,0,csvs)
    with open(csvfile, "a") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(out)
    
from tkinter import Tk, Label, Button, Entry


class Root(Tk):
    def __init__(self):
        super().__init__()
        self.title_label = Label(self, text="A simple eval-based calculator, \nnot for production usage :)")
        self.title_label.pack()
        self.entry = Entry(self)
        self.entry.pack()
        self.entry.insert(0, "")
        self.label = Label(self, text="")
        self.label.pack()
        self.button = Button(self, text="Scrap!", command=self.onclick)
        self.button.pack()

    def onclick(self):
        run(self.entry.get())
        self.label.configure(text=str("Done"))


root = Root()
root.mainloop()