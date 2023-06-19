AWS_REGION := "us-west-2"
AWS_PROFILE := "mlops-club"

cdk COMMAND: require-aws-login
	AWS_PROFILE="{{AWS_PROFILE}}" \
		cdk "{{COMMAND}}" --all --app "python infrastructure/app.py"

install:
	pip install --upgrade pip
	pip install pre-commit flake8 flake8-docstrings Flake8-pyproject radon pylint mypy black isort

open-aws:
    #!/bin/bash
    SSO_AWS_START_URL="https://d-926768adcc.awsapps.com/start"
    open $SSO_AWS_START_URL

require-aws-login:
	#!/bin/bash

	# Step 1: Determine if we are logged in
	OUTPUT=$(aws s3 ls --profile "{{AWS_PROFILE}}" 2>&1)

	# Step 2: If we are not logged in, then login
	if echo "$OUTPUT" | grep -q 'The SSO session associated with this profile has expired or is otherwise invalid.'; then
		just login-to-aws
	fi

# Ensure that an "mlops-club" AWS CLI profile is configured. Then go through an AWS SSO
# sign in flow to get temporary credentials for that profile. If this command finishes successfully,
# you will be able to run AWS CLI commands against the MLOps club account using '--profile mlops-club'
# WARNING: this login only lasts for 8 hours
login-to-aws:
    #!/bin/bash
    SSO_AWS_PROFILE_NAME="{{AWS_PROFILE}}"
    SSO_AWS_ACCOUNT_ID="630013828440"
    SSO_AWS_START_URL="https://d-926768adcc.awsapps.com/start"
    SSO_AWS_REGION="us-west-2"

    # configure an "[mlops-club]" profile in aws-config
    echo "[mlops-club] Configuring an AWS profile called '${SSO_AWS_PROFILE_NAME}'"
    aws configure set sso_start_url ${SSO_AWS_START_URL} --profile ${SSO_AWS_PROFILE_NAME}
    aws configure set sso_region ${SSO_AWS_REGION} --profile ${SSO_AWS_PROFILE_NAME}
    aws configure set sso_account_id ${SSO_AWS_ACCOUNT_ID} --profile ${SSO_AWS_PROFILE_NAME}
    aws configure set sso_role_name AdministratorAccess --profile ${SSO_AWS_PROFILE_NAME}
    aws configure set region ${SSO_AWS_REGION} --profile ${SSO_AWS_PROFILE_NAME}

    # login to AWS using single-sign-on
    aws sso login --profile ${SSO_AWS_PROFILE_NAME} \
    && echo '' \
    && echo "[mlops-club] ✅ Login successful. AWS CLI commands will now work by adding the '--profile ${SSO_AWS_PROFILE_NAME}' 😃" \
    && echo "             Your '${SSO_AWS_PROFILE_NAME}' profile has temporary credentials using this identity:" \
    && echo '' \
    && aws sts get-caller-identity --profile ${SSO_AWS_PROFILE_NAME} | cat

install-cdk:
	# install npm
	apt-get update \
		&& apt-get upgrade -y \
		&& apt-get -y install curl dirmngr apt-transport-https lsb-release ca-certificates \
		&& curl -sL https://deb.nodesource.com/setup_18.x | bash - \
		&& apt-get update -y && apt-get install -y nodejs
	npm install -g aws-cdk

get-account-id:
    #!/usr/bin/env python3
    import json
    import subprocess

    args = ["aws", "sts", "get-caller-identity", "--profile", '"{{AWS_PROFILE}}"']
    proc = subprocess.run(args, capture_output=True)
    user_data = json.loads(proc.stdout)
    print(user_data["Account"])

synth-project:
	python .projenrc.py

lint:
	pre-commit run --all-files

lint-ci:
	SKIP=no-commit-to-branch pre-commit run --all-files

tag-with-latest-version:
	git tag $$(cat VERSION.txt) || echo "repository already tagged"

push-tags-to-remote:
	git push origin --tags
