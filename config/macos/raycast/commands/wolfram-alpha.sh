#!/bin/bash

# required parameters:

# @raycast.schemaVersion 1
# @raycast.title Wolfram Alpha
# @raycast.mode fullOutput

# optional parameters:

# @raycast.icon icons/wolfram-alpha.png
# @raycast.argument1 { "type": "text", "placeholder": "query" }
# @raycast.packageName Math

# documentation:

# @raycast.description Use Wolfram Alpha to answer your query
# @raycast.author es183923
# @raycast.authorURL https://github.com/es183923

# configuration

APP_ID="4U453L-75A54TEYU4" # Wolfram Alpha API app id
units="metric" # units (`metric` or `imperial`)
# encode text
encoded_text=$(echo $1 | curl -Gso /dev/null -w %{url_effective} \
--data-urlencode @- "" | cut -c 3- || true)
# search link
link="http://api.wolframalpha.com/v1/result?appid=${APP_ID}&i=${encoded_text}\
&units=${units}"
# query result
echo $(curl -s $link)
