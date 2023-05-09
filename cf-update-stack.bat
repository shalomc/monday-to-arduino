@echo off
set STACK_NAME=monday-to-arduino
set REGION=eu-central-1
set TEMPLATE=cloudformation-monday-to-arduino.yaml
set AWSPROFILE=metamoneta

@call aws cloudformation update-stack --stack-name %STACK_NAME% ^
    --no-use-previous-template ^
    --template-body file://%TEMPLATE% ^
    --capabilities CAPABILITY_IAM ^
    --parameters ParameterKey=APIKEY,UsePreviousValue=true ^
    --profile %AWSPROFILE% ^
    --region %REGION%

@call private\cf-install-in-s3.bat