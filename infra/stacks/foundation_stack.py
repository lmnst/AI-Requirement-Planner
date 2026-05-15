from aws_cdk import (
    CfnOutput,
    Duration,
    RemovalPolicy,
    Stack,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct


GITHUB_REPO = "lmnst/AI-Requirement-Planner"
GITHUB_BRANCH = "main"
GITHUB_OIDC_URL = "https://token.actions.githubusercontent.com"
GITHUB_OIDC_AUD = "sts.amazonaws.com"

ECR_REPO_NAME = "ai-requirement-planner"
SECRET_NAME = "ai-requirement-planner/openai"
DEPLOY_ROLE_NAME = "AiRequirementPlannerGitHubDeployRole"


class FoundationStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.ecr_repo = ecr.Repository(
            self,
            "EcrRepo",
            repository_name=ECR_REPO_NAME,
            image_scan_on_push=True,
            image_tag_mutability=ecr.TagMutability.IMMUTABLE,
            lifecycle_rules=[
                ecr.LifecycleRule(
                    description="Keep last 10 tagged images",
                    max_image_count=10,
                    tag_status=ecr.TagStatus.TAGGED,
                    tag_pattern_list=["*"],
                ),
                ecr.LifecycleRule(
                    description="Expire untagged images after 7 days",
                    max_image_age=Duration.days(7),
                    tag_status=ecr.TagStatus.UNTAGGED,
                ),
            ],
            removal_policy=RemovalPolicy.RETAIN,
        )

        existing_oidc_arn = self.node.try_get_context("existing_github_oidc_arn")
        if existing_oidc_arn:
            oidc_provider = iam.OpenIdConnectProvider.from_open_id_connect_provider_arn(
                self, "GitHubOidcProvider", existing_oidc_arn
            )
        else:
            oidc_provider = iam.OpenIdConnectProvider(
                self,
                "GitHubOidcProvider",
                url=GITHUB_OIDC_URL,
                client_ids=[GITHUB_OIDC_AUD],
            )

        sub_value = f"repo:{GITHUB_REPO}:ref:refs/heads/{GITHUB_BRANCH}"
        principal = iam.OpenIdConnectPrincipal(
            oidc_provider,
            conditions={
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": GITHUB_OIDC_AUD,
                    "token.actions.githubusercontent.com:sub": sub_value,
                }
            },
        )

        deploy_role = iam.Role(
            self,
            "GitHubDeployRole",
            role_name=DEPLOY_ROLE_NAME,
            assumed_by=principal,
            max_session_duration=Duration.hours(1),
            description=(
                f"OIDC deploy role for GitHub Actions on {GITHUB_REPO} "
                f"branch {GITHUB_BRANCH}. CDK-managed."
            ),
        )

        # AdministratorAccess is intentionally broad so first-deploy works without
        # iterating on permission denials. After the pipeline is proven, replace
        # with a least-privilege policy covering: cloudformation on these stacks,
        # ecr on this repo, lambda on this function, apigatewayv2 on this api,
        # logs on this log group, iam:PassRole on the Lambda execution role,
        # secretsmanager:GetSecretValue/DescribeSecret on the openai secret,
        # sts:AssumeRole on cdk-* bootstrap roles. See README OIDC section.
        deploy_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        )

        self.openai_secret = secretsmanager.Secret(
            self,
            "OpenAiSecret",
            secret_name=SECRET_NAME,
            description=(
                "OPENAI_API_KEY for AI-Requirement-Planner Lambda. "
                "Value injected out-of-band via aws secretsmanager put-secret-value, not by CDK."
            ),
            removal_policy=RemovalPolicy.RETAIN,
        )

        CfnOutput(self, "EcrRepoUri", value=self.ecr_repo.repository_uri)
        CfnOutput(self, "EcrRepoArn", value=self.ecr_repo.repository_arn)
        CfnOutput(self, "GitHubDeployRoleArn", value=deploy_role.role_arn)
        CfnOutput(self, "OpenAiSecretArn", value=self.openai_secret.secret_arn)
        CfnOutput(self, "OpenAiSecretName", value=self.openai_secret.secret_name)
