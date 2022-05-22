#/bin/bash

md5sum g1database.db > checksum.md5_g1database

./collect_data.sh

md5sum -c checksum.md5_g1database --status

# Plot data
if [ $? -eq 1 ]
then
    echo "g1database was updated"
    echo ""
    echo "Creating Plots ..."
    ./plot_topics.py
    ./plot_wordcloud.py

    echo "Plots created"
else
    echo "g1database was not updated."
    echo "There is no need to run plot scripts now"
fi
rm checksum.md5_g1database
