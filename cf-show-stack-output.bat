@echo off
set STACK_NAME=monday-to-arduino
set REGION=eu-central-1
set TEMPLATE=cloudformation-monday-to-arduino.yaml
set AWSPROFILE=metamoneta

@call aws cloudformation describe-stacks --stack-name %STACK_NAME% ^
    --profile %AWSPROFILE% ^
    --region %REGION% | jq .Stacks[0].Outputs