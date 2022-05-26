# web scrapping texts from g1.globo.com for NLP

The idea here is to collect many articles from the website
<em>g1.globo.com</em> to apply <strong>NLP</strong> techniques

The set of words here is in portuguese.

After running
```
./database/collect_data.sh
```
A database, using the RDBMS <strong>SQLite3</strong>, called
<em>g1database.db</em> will be created. This database
has only one relation, given by the scheme:
```
create table articles (
    id          TEXT,
    created_at  TEXT, 
    url         TEXT NOT NULL,
    section     TEXT,
    summary     TEXT,
    title       TEXT NOT NULL,
    text        TEXT NOT NULL,

    PRIMARY KEY(id, created_at)
);
```

To run all scripts at once issue the command
```
./run_scripts.sh
```

## Statistics
| **Database statistics**   |      |
| :---                      | :--- |
| Number of texts collected | 398 |

## Plots

+ Plot showing all topics and their frequencies
<div align='center'>
    <img src='imgs/topic_trends.svg'
         width='600px'
         alt='topic trends image'
    />
</div>

+ Plot showing word frequencies -- without the stopwords
<div align='center'>
    <img src='imgs/wordcloud.svg'
         width='600px'
         alt='wordcloud image'
    />
</div>

---

Given the set of bag of word 
I will project them into $R^2$ and
$R^3$ using the truncated SVD transformation.
<div align='center'>
    <img src='imgs/docs_embedded_in_R2.svg'
         width='400px'
         alt='R2 image'
    />
    <img src='imgs/docs_embedded_in_R3.svg'
         width='400px'
         alt='R3 image'
    />
</div>

Despite that low dimension vector spaces loses a lot of structure we 
can still see some topics with a high distance between other topics

Embedding these bag of vectors into $\mathbb{R}^{300}$ we get a better
variance description of the phenomenons. Below a correlation plot 
showing the relation of the $i-th$ features
<div align='center'>
    <img src='imgs/corr_color_map.svg'
         width='400px'
         alt='correlation map image'
    />
</div>

## Dependencies
+ SQLite3
+ Python3 libraries:
    - bs4 
    - requests (download urls)
    - json
    - re
    - sqlite3
+ PERL
+ wget

The programs were tested in a GNU/LINUX machine.
