#!/bin/bash
set -eu
IFS=$'\n\t'

# aws ec2 run-instances \
#     --image-id $DEV_AMI \
#     --instance-type t1.micro \
#     --key-name $DEV_KEYPAIR \
#     --security-groups $DEV_SG \
#     --min-count 0 \
#     --max-count 1 \
 
ec2-run-instances \
    --aws-access-key "$AWS_ACCESS_KEY_ID" \
    --aws-secret-key "$AWS_SECRET_ACCESS_KEY" \
    --group $DEV_SG \
    --instance-type t1.micro \
    --key $DEV_KEYPAIR \
    $DEV_AMI \
