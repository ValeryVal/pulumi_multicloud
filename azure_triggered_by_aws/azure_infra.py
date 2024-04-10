"""An Azure RM Python Pulumi program"""

import pulumi
import pulumi_azure as azure
from azure.identity import DefaultAzureCredential
from azure.mgmt.web import WebSiteManagementClient

resource_group = azure.core.ResourceGroup("resource_group",
                                            location="westeurope",
                                            opts=pulumi.ResourceOptions(protect=True))

storage_azure = azure.storage.Account("storageAzure",
                                      resource_group_name=resource_group.name,
                                      location="westeurope",
                                      access_tier="Hot",
                                      account_tier="Standard",
                                      account_replication_type="LRS")

service_plan = azure.appservice.ServicePlan("az_func_serv_plan",
                                                    resource_group_name=resource_group.name,
                                                    location=resource_group.location,
                                                    os_type="Linux",
                                                    sku_name="Y1")
user_assigned_identity = azure.authorization.UserAssignedIdentity("assigned_identity",
                                                                             location=resource_group.location,
                                                                             resource_group_name=resource_group.name)

linux_function_app = azure.appservice.LinuxFunctionApp("LinuxFuncApp",
                                                               app_settings={
                                                                   "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
                                                               },
                                                               builtin_logging_enabled=False,
                                                               location=resource_group.location,
                                                               resource_group_name=resource_group.name,
                                                               service_plan_id=service_plan.id,
                                                               storage_account_name=storage_azure.name,
                                                               storage_account_access_key=storage_azure.primary_access_key,
                                                               site_config=azure.appservice.LinuxFunctionAppSiteConfigArgs(
                                                                   application_stack=azure.appservice.LinuxFunctionAppSiteConfigApplicationStackArgs(
                                                                       python_version="3.11"
                                                                   ),
                                                                   cors=azure.appservice.LinuxFunctionAppSiteConfigCorsArgs(
                                                                       allowed_origins=["https://portal.azure.com", "*"]
                                                                   ),
                                                               ),
                                                               sticky_settings=azure.appservice.LinuxFunctionAppStickySettingsArgs(
                                                                   app_setting_names=[
                                                                       "APPINSIGHTS_INSTRUMENTATIONKEY",
                                                                       "APPLICATIONINSIGHTS_CONNECTION_STRING ",
                                                                       "APPINSIGHTS_PROFILERFEATURE_VERSION",
                                                                       "APPINSIGHTS_SNAPSHOTFEATURE_VERSION",
                                                                       "ApplicationInsightsAgent_EXTENSION_VERSION",
                                                                       "XDT_MicrosoftApplicationInsights_BaseExtensions",
                                                                       "DiagnosticServices_EXTENSION_VERSION",
                                                                       "InstrumentationEngine_EXTENSION_VERSION",
                                                                       "SnapshotDebugger_EXTENSION_VERSION",
                                                                       "XDT_MicrosoftApplicationInsights_Mode",
                                                                       "XDT_MicrosoftApplicationInsights_PreemptSdk",
                                                                       "APPLICATIONINSIGHTS_CONFIGURATION_CONTENT",
                                                                       "XDT_MicrosoftApplicationInsightsJava",
                                                                       "XDT_MicrosoftApplicationInsights_NodeJS",
                                                                   ],
                                                               ),
                                                               zip_deploy_file='azure_func_http_trigger/function.zip'
                                                               )

