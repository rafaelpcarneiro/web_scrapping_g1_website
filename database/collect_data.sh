#/bin/bash

#today=`date "+%F"`
today=`date "+ day: %Y-%m-%d   time: %H:%M"`
echo "Extracting texts from g1.globo.com"
echo "------ $today"
echo ""

wget -q "https://g1.globo.com/" -O g1.html
perl -n -e 'print $1 if m/({"config":.+}),/' g1.html > g1.json


test ! -e g1database.db && sqlite3 < create_relations.sql

./get_g1_texts.py



### Still saving json files
#fileName="${today}_g1.json"
#jq . g1.json > json_files/$fileName



### Deleting unnecessary files
rm g1.json g1.html

echo "All data collected and stored at -> database/g1database.db"
