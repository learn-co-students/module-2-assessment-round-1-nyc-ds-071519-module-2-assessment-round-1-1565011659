#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 09:40:32 2019

@author: mackenziemitchell
"""

import requests
import json
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup

url = 'https://pokeapi.co/api/v2/pokemon/?limit=151'
results = requests.get(url).json()['results']
results

def get_pokedata(url):
    pokedata={}
    for result in results:
        pokedata={'name':result['name']}
    print(pokedata)
print(results)

pokedata=[]
for result in results:
    res = requests.get(result['url']).json()
    types=[]
    for ty in res['types']:
        types.append(ty['type']['name'])
    abilities=[]
    for ab in res['abilities']:
        abilities.append(ab['ability']['name'])
    pokedata.append({'id':res['id'],'name':result['name'], 'base_experience':res['base_experience'], 'weight':res['weight'], 'height':res['height'], 'types':types, 'abilities':abilities})

class Pokemon():
    def __init__(self, pid, name, exp,weight,height,types,abilities):
        self.pid=pid
        self.name=name
        self.exp=exp
        self.weight=weight
        self.height=height
        self.types=types
        self.abilities=abilities
    def bmi(self):
        return (self.weight/10)/(self.height/10)**2
bulbasaur=Pokemon(1, 'bulbasaur', 64, 69, 7, ['poison', 'grass'],['chlorophyll','overgorw'])
charmander=Pokemon(4, 'charmander', 62, 85, 6, ['fire'],['solar-power','blaze'])
squirtle=Pokemon(7, 'squirtle', 63, 90, 5, ['water'],['rain-dish','torrent'])

def print_pokeinfo(pokemon_object):
    o = pokemon_object
    print('pid: ' + str(o.pid) + '\n' +
          'Name: ' + o.name.title() + '\n' +
          'Base experience: ' + str(o.exp) + '\n' +
          'Weight: ' + str(o.weight) + '\n' +
          'Height: ' + str(o.height) + '\n' +
          'Types: ' + str(o.types) + '\n' +
          'Abilities: ' + str(o.abilities) + '\n'
         )
    
print_pokeinfo(bulbasaur)
print_pokeinfo(charmander)
print_pokeinfo(squirtle)
print(bulbasaur.bmi()) # 14.08
print(charmander.bmi()) # 23.61
print(squirtle.bmi()) # 36

cnx = sqlite3.connect('pokemon.db')
c=cnx.cursor()
q1 = 'SELECT * FROM pokemon WHERE base_experience>200'
pd.read_sql(q1, cnx)
q2 = 'SELECT pid, name, types[0], types[1] FROM pokemon WHERE types[0]==""water"" OR types[1]==""water""'
pd.read_sql(q2, cnx)
q3 = 'SELECT avg(weight) FROM pokemon SORT BY types[0] DESC'
pd.read_sql(q3, cnx)
q4 = 'SELECT name, types[1], ?!?!??!?!?!?!?!'
pd.read_sql(q4, cnx)
q5 = ''
pd.read_sql(q5, cnx)

html_page = requests.get('http://quotes.toscrape.com/') 
# Pass the page contents to beautiful soup for parsing
soup = BeautifulSoup(html_page.content, 'html.parser')
soup.prettify

author=soup.find('small', {'class':'author'})
author.next_sibling.next_sibling['href']
var1=(author.text,author.next_sibling.next_sibling['href'])
var1

def authors(url):
    html_page = requests.get(url) 
    soup = BeautifulSoup(html_page.content, 'html.parser')
    soup.prettify
    authorlist=[]
    for author in soup.findAll('small', {'class':'author'}):
        path=author.next_sibling.next_sibling['href']
        authorlist.append({author.text:path})
    return authorlist

print(authors('http://quotes.toscrape.com/'))
print('\n')
print(authors('http://quotes.toscrape.com/page/3'))

first=[]
for page in range(1,6):
    html_page = requests.get('http://quotes.toscrape.com/page/{}'.format(page)) 
    soup = BeautifulSoup(html_page.content, 'html.parser')
    author=soup.find('small', {'class':'author'})
    first.append(author.text)
first

def get_some_quotes(url):
    html_page = requests.get(url) 
    soup = BeautifulSoup(html_page.content, 'html.parser')
    soup.prettify
    quoteinfo=[]
    for quote in soup.findAll('span',{'class':'text'}):
            quoteinfo.append({'quote':quote.text,'author':quote.next_sibling.next_sibling.text.split('\n')[0][3:]})
    return quoteinfo

quotes_for_mongo = get_some_quotes('http://quotes.toscrape.com/' )
quotes_for_mongo

