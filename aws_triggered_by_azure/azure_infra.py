from pulumi import StackReference

import pulumi
import pulumi_azure as azure

config = pulumi.Config()
organization_name = config.require('organization_name')
from_aws_stack = StackReference(f"{organization_name}/aws_azure_connection/aws")
webhook_url = from_aws_stack.get_output("restAPI url")

resource_group = azure.core.ResourceGroup("resource_group",
                                          location="westeurope",
                                          opts=pulumi.ResourceOptions(protect=False))

storage_acc = azure.storage.Account("storageAcc",
                                    access_tier="Hot",
                                    account_replication_type="RAGRS",
                                    account_tier="Standard",
                                    allow_nested_items_to_be_public=False,
                                    cross_tenant_replication_enabled=False,
                                    location="westeurope",
                                    name="awstriggertest1",
                                    network_rules=azure.storage.AccountNetworkRulesArgs(
                                        bypasses=["AzureServices"],
                                        default_action="Allow",
                                    ),
                                    queue_properties=azure.storage.AccountQueuePropertiesArgs(
                                        hour_metrics=azure.storage.AccountQueuePropertiesHourMetricsArgs(
                                            enabled=True,
                                            include_apis=True,
                                            retention_policy_days=7,
                                            version="1.0",
                                        ),
                                        logging=azure.storage.AccountQueuePropertiesLoggingArgs(
                                            delete=False,
                                            read=False,
                                            version="1.0",
                                            write=False,
                                        ),
                                        minute_metrics=azure.storage.AccountQueuePropertiesMinuteMetricsArgs(
                                            enabled=False,
                                            version="1.0",
                                        ),
                                    ),
                                    resource_group_name=resource_group.name,
                                    opts=pulumi.ResourceOptions(protect=True))

topic = azure.eventgrid.SystemTopic("example",
                                    identity=azure.eventgrid.SystemTopicIdentityArgs(
                                        type="SystemAssigned",
                                    ),
                                    location="westeurope",
                                    name="aws1",
                                    resource_group_name=resource_group.name,
                                    source_arm_resource_id=storage_acc.id,
                                    topic_type="Microsoft.Storage.StorageAccounts",
                                    opts=pulumi.ResourceOptions(protect=True))

subscription = azure.eventgrid.SystemTopicEventSubscription("subsription",
                                                            advanced_filtering_on_arrays_enabled=True,
                                                            included_event_types=[
                                                                "Microsoft.Storage.BlobCreated",
                                                                "Microsoft.Storage.BlobDeleted",
                                                            ],
                                                            name="awsazuresubscription1",
                                                            resource_group_name=resource_group.name,
                                                            retry_policy=azure.eventgrid.SystemTopicEventSubscriptionRetryPolicyArgs(
                                                                event_time_to_live=1440,
                                                                max_delivery_attempts=30,
                                                            ),
                                                            system_topic=topic.name,
                                                            webhook_endpoint=azure.eventgrid.SystemTopicEventSubscriptionWebhookEndpointArgs(
                                                                max_events_per_batch=1,
                                                                preferred_batch_size_in_kilobytes=64,
                                                                url=webhook_url,
                                                                # url=webhook_url.apply(lambda url: url + "auth")
                                                            ),
                                                            opts=pulumi.ResourceOptions(protect=True))
