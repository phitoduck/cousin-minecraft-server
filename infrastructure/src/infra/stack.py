"""Singular CloudFormation stack for this project."""

import aws_cdk as cdk
from constructs import Construct
from infra.settings import Settings


class Stack(cdk.Stack):
    """Singular CloudFormation stack for this project."""

    def __init__(
        self,
        scope: Construct,
        stack_id: str,
        # pylint: disable=unused-argument
        settings: Settings,
        **kwargs,
    ) -> None:
        """
        Init method.

        :param scope: The cdk app in scope.
        :param construct_id: The stack name.
        """
        super().__init__(scope=scope, id=stack_id, **kwargs)
