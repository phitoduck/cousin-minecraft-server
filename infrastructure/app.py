#!python

"""
Define an AWS CDK "Application" (a set of Stacks).

Use this script to deploy the infrastructure for this project to AWS.

```bash
AWS_PROFILE=profile-name cdk deploy --app "python3 path/to/this/app.py"
```
"""

import aws_cdk as cdk
from infra.settings import Settings
from infra.stack import Stack

# pylint: disable=redefined-builtin
from rich import print

APP_SETTINGS = Settings()

print(APP_SETTINGS.dict())

APP = cdk.App()

Stack(
    APP,
    APP_SETTINGS.stack_name,
    settings=APP_SETTINGS,
    description="The infrastructure for cousin-minecraft-server.",
    env=APP_SETTINGS.cdk_env,
)

# Generates the CloudFormation JSON files in the cdk.out/ folder
APP.synth()
