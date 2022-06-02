#!/usr/bin/env python3
# vim: set ts=4 foldmethod=marker:
import sqlite3
import matplotlib.pyplot as plt


### Connect with the database
connectToDatabase = sqlite3.connect('../database/g1database.db')
cursor            = connectToDatabase.cursor()
sql_select_topics ="""
SELECT 
	section, COUNT(*)
FROM
	articles
GROUP BY 
	section
ORDER BY
	COUNT(*) DESC
LIMIT 20"""

topics = cursor.execute(sql_select_topics).fetchall()
#print(f"#topics = {len(topics)}\n")

topic_names  = [topic[0] for topic in topics]
topic_counts = [topic[1] for topic in topics]

#for t in set(topic_names):
#	print(t, '\n')

plt.barh(topic_names, topic_counts)
plt.yticks(rotation=00, fontsize=5)
plt.ylabel('topics (in portuguese)')
plt.xlabel('frequency')
plt.savefig('../imgs/topic_trends.svg', bbox_inches="tight")
