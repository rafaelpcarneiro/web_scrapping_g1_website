#!/usr/bin/env python3
# vim: set ts=4 foldmethod=marker:
import sqlite3
import matplotlib.pyplot as plt


### Connect with the database
connectToDatabase = sqlite3.connect('g1database.db')
cursor            = connectToDatabase.cursor()
sql_select_topics ="""
SELECT 
	section, COUNT(*)
FROM
	articles
GROUP BY 
	section"""

topics = cursor.execute(sql_select_topics).fetchall()

topic_names  = [topic[0] for topic in topics]
topic_counts = [topic[1] for topic in topics]

plt.barh(topic_names, topic_counts)
plt.yticks(rotation=10, fontsize=8)
plt.ylabel('topics (in portuguese)')
plt.xlabel('frequency')
plt.savefig('topic_trends.svg', bbox_inches="tight")
