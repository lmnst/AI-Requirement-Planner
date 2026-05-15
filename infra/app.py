import os
import sys
from pathlib import Path

# Ensure the infra/ directory is on sys.path so `stacks` package resolves even when
# this script is invoked from a different cwd.
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import aws_cdk as cdk  # noqa: E402

from stacks.application_stack import ApplicationStack  # noqa: E402
from stacks.foundation_stack import FoundationStack  # noqa: E402


def main() -> None:
    app = cdk.App()

    account = os.environ.get("CDK_DEFAULT_ACCOUNT") or os.environ.get("CDK_DEPLOY_ACCOUNT")
    region = "eu-central-1"
    env = cdk.Environment(account=account, region=region)

    foundation = FoundationStack(
        app,
        "AiRequirementPlannerFoundation",
        env=env,
    )

    image_tag = app.node.try_get_context("image_tag")
    image_digest = app.node.try_get_context("image_digest")
    skip_application = str(app.node.try_get_context("skip_application")).lower() == "true"

    # ApplicationStack is only instantiated when we actually have an image to deploy.
    # Without image_tag/image_digest, CDK commands targeting it will simply report
    # "no such stack", which is a clearer error than raising during synth and also
    # lets bootstrap, list, and FoundationStack-only operations proceed unblocked.
    if not skip_application and (image_tag or image_digest):
        ApplicationStack(
            app,
            "AiRequirementPlannerApplication",
            env=env,
            ecr_repo=foundation.ecr_repo,
            openai_secret=foundation.openai_secret,
            image_tag=image_tag,
            image_digest=image_digest,
        )

    app.synth()


if __name__ == "__main__":
    main()
