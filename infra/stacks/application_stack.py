from typing import Optional

from aws_cdk import (
    CfnOutput,
    Duration,
    RemovalPolicy,
    Stack,
    aws_apigatewayv2 as apigwv2,
    aws_apigatewayv2_integrations as apigwv2_integrations,
    aws_ecr as ecr,
    aws_lambda as lambda_,
    aws_logs as logs,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct


FUNCTION_NAME = "ai-requirement-planner"


class ApplicationStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        ecr_repo: ecr.IRepository,
        openai_secret: secretsmanager.ISecret,
        image_tag: Optional[str] = None,
        image_digest: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if not (image_tag or image_digest):
            raise ValueError(
                "ApplicationStack requires either image_tag or image_digest context"
            )

        log_group = logs.LogGroup(
            self,
            "FunctionLogGroup",
            log_group_name=f"/aws/lambda/{FUNCTION_NAME}",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Prefer digest when both are provided; digest is deterministic.
        tag_or_digest = image_digest or image_tag
        code = lambda_.DockerImageCode.from_ecr(
            repository=ecr_repo,
            tag_or_digest=tag_or_digest,
        )

        fn = lambda_.DockerImageFunction(
            self,
            "Function",
            function_name=FUNCTION_NAME,
            code=code,
            memory_size=1024,
            timeout=Duration.seconds(30),
            architecture=lambda_.Architecture.X86_64,
            environment={
                "OPENAI_SECRET_NAME": openai_secret.secret_name,
                "LOG_LEVEL": "INFO",
            },
            log_group=log_group,
        )

        openai_secret.grant_read(fn)

        integration = apigwv2_integrations.HttpLambdaIntegration(
            "LambdaIntegration", handler=fn
        )

        http_api = apigwv2.HttpApi(
            self,
            "HttpApi",
            api_name=f"{FUNCTION_NAME}-http-api",
            default_integration=integration,
        )

        CfnOutput(self, "ApiUrl", value=http_api.api_endpoint)
        CfnOutput(self, "FunctionName", value=fn.function_name)
        CfnOutput(self, "LogGroupName", value=log_group.log_group_name)
