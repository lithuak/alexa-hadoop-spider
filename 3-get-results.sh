#!/bin/bash

# get bucket name
if [ -z "$1" ]
then 
    echo "usage: $0 bucket_name"
    exit
fi

BUCKET=$1

# get files
s3cmd sync s3://$BUCKET/output .

rm output/_SUCCESS

