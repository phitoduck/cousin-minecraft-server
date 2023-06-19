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

MinecraftPaasStack(
   APP,
   APP_SETTINGS.stack_name,
   # login_page_domain_name_prefix just needs to be unique across all AWS accounts
   login_page_domain_name_prefix=APP_SETTINGS.login_domain_prefix,
   env=APP_SETTINGS.cdk_env,
   minecraft_data_bucket_name=APP_SETTINGS.backups_bucket_name,
   description="The infrastructure for cousin-minecraft-server.",
)

# Stack(
#     APP,
#     APP_SETTINGS.stack_name,
#     settings=APP_SETTINGS,
#     description="The infrastructure for cousin-minecraft-server.",
#     env=APP_SETTINGS.cdk_env,
# )

# Generates the CloudFormation JSON files in the cdk.out/ folder
APP.synth()
