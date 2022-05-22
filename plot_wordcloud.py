#!/usr/bin/env python3
# vim: set ts=4 foldmethod=marker:
import sqlite3
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
from wordcloud import WordCloud

# Stopwords
stopwords = set([])
with open('stopwords.txt', 'r') as f:
	stopwords.update( f.read().splitlines() )


### Connect with the database
connectToDatabase = sqlite3.connect('g1database.db')
cursor            = connectToDatabase.cursor()
sql_select_texts ="""
SELECT 
	text
FROM
	articles"""

# Fetch the data
all_texts = cursor.execute(sql_select_texts).fetchall()

# Build the cloud
text  = " ".join( [t[0] for t in all_texts] ).replace('"', " ")



### Saving stopword candidates
#words = text.split()
#stopwords = open('stopwords.txt', 'w')
#count     = np.ones_like( len(words) )
#df        = pd.DataFrame( {'words': words, 'count': count} )
#stopwords = df.groupby('words').sum().sort_values('count') 
#stopwords.to_csv('stopwords.csv')


wordcloud = WordCloud(stopwords=stopwords,
					  background_color='white').generate(text)

plt.imshow(wordcloud, interpolation='bilinear')
plt.subplots_adjust(bottom=0, top=1, left=0, right=1)
plt.tight_layout()

plt.axis('off')
plt.savefig('wordcloud.svg')
