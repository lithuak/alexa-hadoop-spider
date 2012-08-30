#!/bin/bash

# get bucket name
if [ -z "$1" ]
then 
    echo "usage: $0 bucket_name"
    exit
fi

BUCKET="s3://$1"

# extract first 100K urls from Alexa archive
unzip -p data/top-1m.csv.zip | head -n 100000 | perl -pe 's/^.*?,//' > data/100K.txt

# delete target bucket
s3cmd rb --force $BUCKET

# create bucket structure for task
s3cmd mb $BUCKET
s3cmd put data/100K.txt $BUCKET/input/100K.txt
s3cmd put mapper.py $BUCKET/job/mapper.py
s3cmd put configure-python.sh $BUCKET/job/configure-python.sh

# bugs.js file must go into mapper's directory 
cd data
jar cf bugs.jar bugs.js 
s3cmd put bugs.jar $BUCKET/input/bugs.jar
cd ..

# a hack to create empty "directory" in S3
touch /tmp/_placeholder
s3cmd put /tmp/_placeholder $BUCKET/log/_placeholder
rm /tmp/_placeholder

