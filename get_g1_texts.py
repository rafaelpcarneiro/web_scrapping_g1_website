#!/usr/bin/env python3
# vim: set ts=4 foldmethod=marker:

from bs4 import BeautifulSoup

import requests #download urls
import json
import re

import sqlite3

# Open json database and store it into a dictionary
json_file = open('g1.json', 'r')
g1        = json.load(json_file)
json_file.close()

# I will be interested into the following values: 
# items
#    |
#     -- id,
#    |
#     -- created 
#    |
#     -- content
#           |
#            -- section
#           |
#            -- summary
#           |
#            -- title
#           |
#            -- url

items = g1['items']

conn   = sqlite3.connect('g1database.db')
cursor = conn.cursor()
sql_command = "INSERT INTO articles(id, created_at, url, section, summary, title, text) \
			   VALUES (?, ?, ?, ?, ?, ?, ?)"

for article in items:
	try:
		url = article['content']['url']
	except:
		continue
	
	id      = article['id']
	created = article['created']
	
	try:
		section = article['content']['section']
	except:
		section = None
	
	try:
		summary = article['content']['summary']
	except:
		summary = None
	
	title   = article['content']['title']
	
	r    = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	#soup = BeautifulSoup(htmlFile, 'lxml')
	
	pTags = soup.body.find_all("p", class_='content-text__container')  #list of <p>
	
	text = ''
	for pTag in pTags:
		checkAd = re.search('.*WhatsApp.*Telegram.*', pTag.text)
		if (pTag.find('h2') is None) & (checkAd is None):
			text += pTag.text
			text += '\n\n'
	
	
	try:
		checkEmptyString = re.search('^\s*$', text)
		if checkEmptyString is None:
			cursor.execute(sql_command, [id, created, url, section, summary, title, text])
	except:
		continue
	#print(title)
	#print(url)
	#print('-' * 80)
	#if checkEmptyString is None:
	#    print(text)
	#    print('\n\n')

conn.commit()
conn.close()

