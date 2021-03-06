#/bin/bash

cd database
md5sum g1database.db > .checksum.md5_g1database

./collect_data.sh

md5sum -c .checksum.md5_g1database --status
databaseUpdated=$?

rm .checksum.md5_g1database

cd ..

# Plot data
if [ $databaseUpdated -eq 1 ]
then
    echo "g1database was updated"
    echo ""
    echo "Creating Plots ..."

    cd plots
    ./plot_topics.py
    ./plot_wordcloud.py

    echo "Plots created"
    echo ""
    cd ..

    echo "Embedding vectors into RN"
    echo ""
    cd embedding_docs_into_RN/
    ./embedding01.py
    cd ..

    # Update readme statistics
    cd configs
    sqlite3 ../database/g1database.db < databaseSize.sql
    databaseSize=`cat databaseSize.txt`
    sed "s/<DATABASESIZE>/$databaseSize/" README.md.template  > \
                                         ../README.md
    cd ..
else
    echo "g1database was not updated."
    echo "There is no need to run plot scripts now"
fi

