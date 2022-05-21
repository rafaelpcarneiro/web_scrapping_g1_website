# web scrapping texts from g1.globo.com for NLP

The idea here is to collect many articles from the website
<em>g1.globo.com</em> to apply <strong>NLP</strong> techniques

The set of words here is is portuguese.

After running
```
./collect_data.sh
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
