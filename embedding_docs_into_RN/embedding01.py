#!/usr/bin/env python3
# vim: set ts=4 foldmethod=marker:
import sqlite3

import matplotlib.pyplot  as     plt
from   matplotlib.colors  import cnames

import pandas as pd
import numpy  as np

from sklearn.pipeline                import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition           import PCA, TruncatedSVD

### The stopword list
stopwords = set([])
with open('../stopwords.txt', 'r') as f:
	stopwords.update( f.read().splitlines() )


### Connecting with the database
connectToDatabase = sqlite3.connect('../database/g1database.db')
cursor            = connectToDatabase.cursor()
sql_select_texts = """
	SELECT 
		section, text
	FROM
		articles
	WHERE
		section IN (
			SELECT
				X.section 
			FROM 
				articles AS X
			GROUP BY 
				X.section
			ORDER BY
				COUNT(*) DESC
			LIMIT 20
		)"""

### Fetching data and storing it
sql_result = cursor.execute(sql_select_texts).fetchall()


texts = [
	t[1].lower().
	     replace('"', " ").
	     replace(':', " ") 
	for t in sql_result 
]


target = [
	t[0] 
	for t in sql_result
]

data = pd.DataFrame({
	'texts': texts,
	'target': target
})
	
target_class = set(target) 

### Running the model
ml_model = [
	Pipeline([
		('bag_of_words', CountVectorizer(stop_words = list( stopwords ) )),
		('tfidf',        TfidfTransformer() ),
		('vec_transf',   TruncatedSVD(n_components = 2,
									  algorithm = 'arpack',
									  random_state = 99))
	]),
	Pipeline([
		('bag_of_words', CountVectorizer(stop_words = list( stopwords ) )),
		('tfidf',        TfidfTransformer() ),
		('vec_transf',   TruncatedSVD(n_components = 3,
									  algorithm = 'arpack',
									  random_state = 99))
	])
]


####### Running and Plotting all ml_models

### Selecting colors
randomColor = np.random.RandomState(99)

color_list = randomColor.choice( 
	list( cnames.keys() ),
	len( target_class ),
	False
)

target_color_map = dict( 
	zip( target_class, color_list)
)


### Running models
model_index = 0
for model in ml_model:

	model.fit(data.texts)

	docs_RN = model.transform(data.texts)

	if (model_index == 1):
		fig    = plt.figure()
		ax     = plt.axes(projection="3d")

	for target in target_class:
		index_target = data.index[data.target == target].values

		if (model_index == 1):
			ax.scatter3D( 
				docs_RN[index_target, 0], 
				docs_RN[index_target, 1], 
				docs_RN[index_target, 2], 
				c = target_color_map[target],
				label = target,
				s=12
			)
		elif (model_index == 0): 
			plt.scatter( 
				docs_RN[index_target, 0], 
				docs_RN[index_target, 1], 
				c = target_color_map[target],
				s=12,
				label = target
			)
	if (model_index == 0):
		plt.legend(
			loc            = 'center left',
			bbox_to_anchor = (1, 0.5),
			fontsize       = 'xx-small'
		)
		plt.tight_layout()
		plt.savefig("../imgs/docs_embedded_in_R2.svg")
		plt.close()
	else:
		plt.legend(
			loc            = 'center left',
			bbox_to_anchor = (1, 0.5),
			fontsize       = 'xx-small'
		)
		plt.tight_layout()
		plt.savefig("../imgs/docs_embedded_in_R3.svg")
		plt.close()

	model_index += 1
	print( model['vec_transf'].explained_variance_ratio_.sum())

#plt.legend()
#plt.xlim([-1,10])

#print(z.explained_variance_ratio_)

### Last model
model = Pipeline([
	('bag_of_words', CountVectorizer(stop_words = list( stopwords ) )),
	('tfidf',        TfidfTransformer() ),
	('vec_transf',   TruncatedSVD(n_components = 300, random_state = 99))
])

doc_R300 = model.fit_transform(data.texts)
fig, ax  = plt.subplots(figsize=(8,8))

im = ax.imshow(
	np.cov(doc_R300),
	interpolation='nearest'
)

fig.colorbar(
	im,
	orientation='vertical',
	fraction = 0.05
)

plt.savefig('../imgs/corr_color_map.svg')



