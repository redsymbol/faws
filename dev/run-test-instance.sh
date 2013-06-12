#!/bin/bash
set -eu
IFS=$'\n\t'

ec2-run-instances \
    --aws-access-key "$AWS_ACCESS_KEY_ID" \
    --aws-secret-key "$AWS_SECRET_ACCESS_KEY" \
    --instance-type t1.micro \
    $DEV_AMI \
