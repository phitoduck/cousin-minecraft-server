#!python

"""
Define an AWS CDK "Application" (a set of Stacks).

Use this script to deploy the infrastructure for this project to AWS.

```bash
AWS_PROFILE=profile-name cdk deploy --app "python3 path/to/this/app.py"
```
"""

import aws_cdk as cdk
from cdk_minecraft import MinecraftPaasStack

# pylint: disable=redefined-builtin
from rich import print

from infra.settings import Settings
from infra.stack import Stack

APP_SETTINGS = Settings()

print(APP_SETTINGS.dict())

APP = cdk.App()

data_stack = Stack(
    APP,
    "cousins-server-data",
    env=APP_SETTINGS.cdk_env,
    description=f"Data for {APP_SETTINGS.stack_name}",
)

MinecraftPaasStack(
    APP,
    APP_SETTINGS.stack_name,
    login_page_domain_name_prefix=APP_SETTINGS.login_domain_prefix,
    env=APP_SETTINGS.cdk_env,
    minecraft_data_bucket_name=data_stack.game_data_bucket_name,
    ssh_key_pair_name=APP_SETTINGS.ssh_key_pair_name,
    top_level_custom_domain_name=APP_SETTINGS.custom_domain_name,
    minecraft_server_version="1.20.1",
    description="The infrastructure for cousin-minecraft-server.",
)

# Generates the CloudFormation JSON files in the cdk.out/ folder
APP.synth()
