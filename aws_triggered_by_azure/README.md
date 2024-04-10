### Prerequisites

For this project you should have installed [Pulumi](https://www.pulumi.com/docs/install/),
[AWS CLI and credentials](https://www.pulumi.com/registry/packages/aws/installation-configuration/#credentials), 
[Azure CLI or another option to authenticate](https://www.pulumi.com/registry/packages/azure-native/installation-configuration/#authentication-methods)

Create a new stack:
```
pulumi stack init aws
```
and
```
pulumi stack init azure
```

install requirements
```
pip install -r .\requirements.txt
```

Then you can implement using all infrastructure if this project:
```
pulumi up
```

To see stacks and the current one:
```
pulumi stack ls
```

To choose particular stack:
```
pulumi stack select stackname
```

In this project are two stacks: aws and azure. 
You should start to deploy from aws to create webhook url 
and then switch to azure stack and deploy it. 

You also need to change value of aws_azure_connection:organization_name: in Pulumi.aws.yaml.


### Description of The Project

This infrastructure is used for triggering AWS Lambda 
with restAPI webhook that is triggerred by uploading 
or deleting file in Azure Blob Storage. 

The schema is:
Uploading/deleting file in Azure Blob Storage ->
Azure Event Grid Subscription Topic gives a request to webhook url->
webhook url is AWS APIGateway url ->
which triggers AWS Lambda.

Pulumi project has two stacks: aws and azure. In aws stack APIGateway webhook url 
should be created and transferred to Azure stack to be used in Azure Eventgrid topic.
When connecting webhook handshake is happening so url should return
validation code and status 200. 

For this we have lambda_code/webhook_auth.py code for lambda to implement this handshake.
You should set handler in your lambda_function resource to "webhook_auth.lambda_handler"
during first deployment to aws and azure. Then you can change handler to your main logic
e.g. "lambda_function.lambda_handler".