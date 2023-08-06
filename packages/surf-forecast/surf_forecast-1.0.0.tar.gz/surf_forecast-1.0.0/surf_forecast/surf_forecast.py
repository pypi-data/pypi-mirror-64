import json 
import requests
import mechanize
from bs4 import BeautifulSoup

def fetch(city):
    
    # Selects city
    br = mechanize.Browser()
    br.open('https://www.surf-forecast.com')
    
    def select_form(form):
        return form.attrs.get('action', None) == '/breaks/catch'

    br.select_form(predicate=select_form)
    
    br.form["query"] = city

    res = br.submit()
    
    # Requests data from page
    content = res.read()
    soup = BeautifulSoup(content, 'html.parser')

    # Grabs data
    if soup.find("span", {"class": "tempu"}).text == "C":
        unit = "celsius"

    elif soup.find("span", {"class": "tempu"}).text == "F":
        unit = "fahrenheit"

    sea = soup.find("span", itemprop="name").text[:-1].lower()
    temp = soup.select(".temp")[0].text
    temp_mean = soup.select(".temp")[1].text
    temp_max = soup.select(".temp")[2].text
    temp_min = soup.select(".temp")[3].text

    # Returns json of data
    data = {
        'sea': sea,
        'unit': unit,
        'temp': float(temp),
        'temp_mean': float(temp_mean),
        'temp_min': float(temp_min),
        'temp_max': float(temp_max)
    }

    data = json.dumps(data, indent=1)
    

    return data