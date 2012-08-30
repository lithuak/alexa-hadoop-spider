#!/bin/bash

# get bucket name
if [ -z "$1" ]
then 
    echo "usage: $0 bucket_name"
    exit
fi

BUCKET=$1

# delete previous output (otherwise jobflow will fail to start)
s3cmd del --recursive --force "s3://$BUCKET/output" 

# run job
elastic-mapreduce --create --stream \
--input "s3n://$BUCKET/input/100K.txt" \
--output "s3n://$BUCKET/output" \
--mapper "s3n://$BUCKET/job/mapper.py" \
--cache-archive "s3n://$BUCKET/input/bugs.jar#data" \
--log-uri "s3n://$BUCKET/log" \
--reduce NONE \
--arg -Dmapred.reduce.tasks=0 \
--bootstrap-action s3n://$BUCKET/job/configure-python.sh \
--instance-group master --instance-count 1 --instance-type m1.small \
--instance-group core --instance-count 19 --instance-type c1.xlarge --bid-price 0.10 \
--enable-debugging

