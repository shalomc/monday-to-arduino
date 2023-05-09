@echo off
set STACK_NAME=sqs-lambda
set REGION=us-west-2
set TEMPLATE=cloudformation-unified-lambda.yaml
set AWSPROFILE=default

@call aws cloudformation describe-stacks --stack-name %STACK_NAME% ^
    --profile %AWSPROFILE% ^
    --region %REGION% | jq .Stacks[0].Outputs