import json

import pulumi
import pulumi_aws_apigateway as apigateway

import pulumi_aws as aws

lambda_code_archive = pulumi.AssetArchive(
    {
        "lambda_function.py": pulumi.FileAsset("./lambda_code/lambda_function.py"),
        "webhook_auth.py": pulumi.FileAsset("./lambda_code/webhook_auth.py"),
    }
)
# An execution role to use for the Lambda function
role = aws.iam.Role("role",
                    assume_role_policy=json.dumps({
                        "Version": "2012-10-17",
                        "Statement": [{
                            "Action": "sts:AssumeRole",
                            "Effect": "Allow",
                            "Principal": {
                                "Service": "lambda.amazonaws.com",
                            },
                        }],
                    }),
                    managed_policy_arns=[aws.iam.ManagedPolicy.AWS_LAMBDA_BASIC_EXECUTION_ROLE])

# A Lambda function to invoke
lambda_function = aws.lambda_.Function("lambda_function",
                          runtime="python3.9",
                          # handler="lambda_function.lambda_handler",
                          handler="webhook_auth.lambda_handler",
                          role=role.arn,
                          code=lambda_code_archive)
cloud_watch = aws.cloudwatch.LogGroup("cloudwatch",
                                  name=f"/aws/lambda/function",
                                  retention_in_days=14)
lambda_logging = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
    effect="Allow",
    actions=[
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
    ],
    resources=["arn:aws:logs:*:*:*"],
)])
lambda_logging_policy = aws.iam.Policy("lambda_logging",
                                       name="lambda_logging",
                                       path="/",
                                       description="IAM policy for logging from a lambda",
                                       policy=lambda_logging.json)
lambda_logs = aws.iam.RolePolicyAttachment("lambda_logs",
                                           role=role.name,
                                           policy_arn=lambda_logging_policy.arn)


api = apigateway.RestAPI("api",
                         routes=[
                             apigateway.RouteArgs(path="/", method=apigateway.Method.POST, event_handler=lambda_function)
                         ])
pulumi.export("restAPI url", api.url)
