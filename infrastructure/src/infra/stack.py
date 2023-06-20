"""Singular CloudFormation stack for this project."""

import aws_cdk as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct


class Stack(cdk.Stack):
    """Singular CloudFormation stack for this project."""

    def __init__(
        self,
        scope: Construct,
        stack_id: str,
        **kwargs,
    ) -> None:
        """
        Init method.

        :param scope: The cdk app in scope.
        :param construct_id: The stack name.
        """
        super().__init__(scope=scope, id=stack_id, **kwargs)

        game_data_bucket = s3.Bucket(
            self,
            "GameDataBucket",
            removal_policy=cdk.RemovalPolicy.RETAIN,
        )

        self.game_data_bucket_name = game_data_bucket.bucket_name
