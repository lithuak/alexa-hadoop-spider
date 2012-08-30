spider.io
=========

An Python/Amazon EMR based crawler for fetching/analyzing big list of urls

Prerequisites
-------------

You should have 3cmd and elastic-mapreduce utils installed on your box and
configured to work with your Amazon EC2 account.

You should pick up the name for the bucket in which the data will be uploaded
and the results will be stored.

Preparing data
--------------

Download the archive of 1M most popular sites from Alexa and put it in the
'data' folder without any modifications.

Take the 'bugs.js' file (you know where to get it) and put it to the same
'data' folder.

Run 1-prepare.sh. The script will prepare the data and upload it to the bucket.

Running Crawler
---------------

Run 2-run-job-flow.sh

Getting Results
---------------

Run 3-get-results.sh. The script will download result files into 'output'
folder.

Last Step
---------

Run 4-analyze.py. The script will take files from 'output' folder, join them
into 'result.json' file and put it in the current directory. At the end the
script will show some statistics.

