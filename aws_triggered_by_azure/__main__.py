"""Multicloud Python Pulumi program"""

import pulumi

config = pulumi.Config()
provider_name = config.require('provider')

if provider_name == "aws":
    import aws_infra

if provider_name == "azure":
    import azure_infra
