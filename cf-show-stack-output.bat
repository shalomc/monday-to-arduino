@echo off
set STACK_NAME=monday-to-arduino
set REGION=eu-central-1
set TEMPLATE=cloudformation-monday-to-arduino.yaml
set AWSPROFILE=metamoneta

@call aws cloudformation describe-stacks --stack-name %STACK_NAME% ^
    --profile %AWSPROFILE% ^
    --region %REGION% | jq ".Stacks[].Outputs[].OutputValue"

rem jq ".Stacks[] | select(.StackName == \"%STACK_NAME%\") | .Outputs[] | select(.OutputKey == \"SQSURL\") | .OutputValue"
rem    jq .Stacks[0].Outputs