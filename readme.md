##Monday to Arduino

### Installation of the Cloudformation template
Log into your AWS account and click one of the following URL for a quick installation in the some popular regions. 
After the Cloudformation stack is active, check the stack outputs for the URLs to use for writing events and for reading events. 

Install in us-east-1:  
https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateURL=https://public-arduino-shalom.s3.eu-central-1.amazonaws.com/cloudformation-monday-to-arduino.yaml&stackName=monday-to-arduino

Install in Frankfurt, eu-central-1: 
https://eu-central-1.console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/quickcreate?templateURL=https://public-arduino-shalom.s3.eu-central-1.amazonaws.com/cloudformation-monday-to-arduino.yaml&stackName=monday-to-arduino

### Installation of the python script
The `check_events_activate_arduino.py` script has several prerequisites. 

Use pip to install them 

    # to install in the python environment
    pip install -r requirements.txt
    
    # to install in this directory
    pip install -r requirements.txt -t .

