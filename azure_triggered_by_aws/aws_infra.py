"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

config = pulumi.Config()
region = config.require('region')
account_id = config.require('account_id')
topic_name = config.require('topic_name')
organization_name = config.require('organization_name')
project_name = config.require('project_name')
azure_function_url = config.require('azure_function_url')

bucket = aws.s3.Bucket("bucket",
                       arn="arn:aws:s3:::aws-trigger-azure",
                       request_payer="BucketOwner",
                       server_side_encryption_configuration=aws.s3.BucketServerSideEncryptionConfigurationArgs(
                           rule=aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
                               apply_server_side_encryption_by_default=aws.s3.
                               BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
                                   sse_algorithm="AES256",
                               ),
                           ),
                       ),
                       opts=pulumi.ResourceOptions(protect=True))

topic_policy = aws.iam.get_policy_document_output(statements=[aws.iam.GetPolicyDocumentStatementArgs(
    effect="Allow",
    principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
        type="Service",
        identifiers=["s3.amazonaws.com"],
    )],
    actions=["SNS:Publish"],
    resources=[f"arn:aws:sns:{region}:{account_id}:{topic_name}"],
    conditions=[aws.iam.GetPolicyDocumentStatementConditionArgs(
        test="ArnLike",
        variable="aws:SourceArn",
        values=[bucket.arn],
    )],
)])

aws_trigger_azure_topic = aws.sns.Topic(
    "aws_trigger_azure_topic",
    name=topic_name,
    policy=topic_policy.json,
    opts=pulumi.ResourceOptions(protect=True)
)


aws_trigger_azure_bucket_topic_subscription = aws.sns.TopicSubscription(
    "aws_trigger_azure_bucket_topic_subscription",
    endpoint=azure_function_url,
    protocol="https",
    topic=aws_trigger_azure_topic.arn,
    opts=pulumi.ResourceOptions(protect=True)
)

bucket_notification = aws.s3.BucketNotification("bucket_notification",
    bucket=bucket.id,
    topics=[aws.s3.BucketNotificationTopicArgs(
        topic_arn=aws_trigger_azure_topic.arn,
        events=["s3:ObjectCreated:*", "s3:ObjectRemoved:*"],
        filter_suffix=".log",
    )])
