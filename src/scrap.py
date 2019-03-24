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


def look(links,textblock):
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
        url_google_maps =( "https://maps.googleapis.com/maps/api/geocode/json?address="+ calle.replace(' ','+') + '+cordoba' +',+CA&key=' + key)
        
        with urllib.request.urlopen(url_google_maps) as url:
            data = json.loads(url.read().decode())
            lat = data['results'][0]['geometry']['location']['lat']
            lng = data['results'][0]['geometry']['location']['lng']
            dormitorios =soup.find(string=re.compile('ormitorios')).find_next('span').text.strip()
            textblock.text = ('new appartement')
            
            save([precio, barrio, calle, dormitorios, links, lat, lng])
    except:
        pass


def save(l):
    csvfile = dir_path + '/deptos.csv'
    
    with open(csvfile, "a") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(l)

def general(page,counts,textblock):

    counts = counts +1
    page = urllib2.urlopen(page)
    soup = BeautifulSoup(page, 'html.parser')

    
    CD=  soup.find('div',class_='CD').find_all('div',class_='Modelo')
    for i in CD:
        look(i.find('a').attrs['href'],csvs )
    if counts <1:
        next_page = 'http://clasificados.lavoz.com.ar' +soup.find('li',class_='pager-next').find('a').attrs['href']
        time.sleep(2)
        textblock.text = "New page"
        general(next_page,counts,textblock)
        
    return csvs

csvs = []
csvs.append(["precio", "barrio", "calle", "dormitorios", "links", "lat", "lng"])




def run(quote_page,textblock):
    textblock.text = "working"
    if  quote_page is not None and quote_page:
        csvfile = dir_path + '/deptos.csv'
        out= general(quote_page,0,textblock)
      
            
