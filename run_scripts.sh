#/bin/bash

./collect_data.sh

# Plot data
echo ""
echo "Creating Plots ..."
./plot_topics.py
./plot_wordcloud.py

echo "Plots created"
