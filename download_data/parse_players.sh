#!/bin/bash

# bin_dir="/$HOME/bin"
bin_dir="/usr/local/bin"

pup_path='.competitors tbody tr json{}'

# Debugging
# "$bin_dir/pup" "$pup_path" | \
#     "$bin_dir/jq" '.[1:]' | "$bin_dir/jq" '.[0]'
# exit 0

"$bin_dir/pup" "$pup_path" | \
    "$bin_dir/jq" '[.[] | {

        cut_element: .children[0].children[0].class,
        cut_score: .children[4].text,
        pos: .children[1].text,
        player: .children[3].children[1].text,
        country_flag_image: .children[3].children[0].src,
        link: .children[3].children[1].href,
        to_par: .children[4].text,
        today: .children[5].text,
        thru: .children[6].text,
        r1: .children[7].text,
        r2: .children[8].text,
        r3: .children[9].text,
        r4: .children[10].text,
        tot: .children[11].text,
         
    }]'
