@echo off
set STACK_NAME=sqs-lambda
set REGION=us-west-2
set TEMPLATE=cloudformation-unified-lambda.yaml
set AWSPROFILE=default

@call aws cloudformation update-stack --stack-name %STACK_NAME% ^
    --no-use-previous-template ^
    --template-body file://%TEMPLATE% ^
    --capabilities CAPABILITY_IAM ^
    --parameters ParameterKey=APIKEY,UsePreviousValue=true ^
    --profile %AWSPROFILE% ^
    --region %REGION%