#!/bin/bash

# Data source
url="https://www.espn.com/golf/leaderboard"

# Current directory
dir_base=$(dirname "$BASH_SOURCE")

# Data dir, `data`, where all files are saved
dir_data="$dir_base/data"
mkdir -p "$dir_data"

# Filenames
filename="data_new.json"
filename_softlink="data.json"

# Download HTML, parse the players, add attribution/timestamps, save to timestamped filename
curl -Ss "$url" | "$dir_base/parse_players.sh" | /usr/local/bin/jq "{
        last_updated: \"$timestamp_seconds\",
        last_updated_str: \"$timestamp_iso\",
        data_source: \"$url\",
        players: .
    }" > "$dir_data/$filename"

# Move into `data` directory
pushd "$dir_data" > /dev/null
# Remove any existing softlink
if [ -e "$filename_softlink" ]
then
    rm "$filename_softlink"
fi
# Soft link `data.json` to point to the current timestamped filename
ln -s "$filename" "$filename_softlink"
# Pop back out of the `data` directory
popd > /dev/null