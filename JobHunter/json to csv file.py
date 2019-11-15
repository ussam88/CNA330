import csv
import json
import urllib.request
import lib

with urllib.request.urlopen ( "https://jobs.github.com/positions.json?location=seattle" ) as url:
    json_data=json.loads ( url.read ().decode () )
    i=(json.dumps ( json_data, indent = 4, sort_keys = True ))
    with open('jobdata.xml', "w") as text_file:
        text_file.write(i)
