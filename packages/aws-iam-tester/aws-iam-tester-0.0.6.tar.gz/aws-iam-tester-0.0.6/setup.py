# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_iam_tester']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.12.22,<2.0.0',
 'click>=7.1.1,<8.0.0',
 'pyyaml>=5.3,<6.0',
 'termcolor>=1.1.0,<2.0.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['aws_iam_tester = aws_iam_tester.cli:main']}

setup_kwargs = {
    'name': 'aws-iam-tester',
    'version': '0.0.6',
    'description': 'AWS IAM tester - simple command-line tool to check permissions handed out to IAM users and roles.',
    'long_description': '# Testing AWS IAM policies\n\n## Introduction\n\nAWS IAM policies are notouriously complex, it is too easy to add some unintended permissions and it is surprisingly difficult to identify these in heavily used AWS accounts.\n\nEven more surprisingly I couldn\'t find a ready-to-use utility that I could leverage.\n\nHence I created one myself.\n\n## Testing approach\n\nThe testing leverages AWS\' [IAM simulator (api)](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html), that basically includes the same IAM evaluation logic that is applied when working in the console or using the cli. The beneits of this approach are:\n\n- It takes all different levels of policies into account. Think about permission boundaries, service control policies and so on.\n- It is an official service from AWS, so you can expect this to kept up to date over time.\n- The actual actions are evaluated, but NOT executed. Hence no need for cleaning up resources after testing.\n\n## Configuration\n\nIn order to run, a configuration of the tests to run is required.\n\nA sample configuration (with only one test) is shown below.\n\n```yaml\n---\nuser_landing_account: 0123456789 # ID of AWS Account that is allowed to assume roles in the test account\nglobal_exemptions: # The roles and/or users below will be ignored in all tests. Regular expressions are supported\n- "^arn:aws:iam::(\\\\d{12}):user/(.*)(ADMIN|admin)(.*)$"\n- "^arn:aws:iam::(\\\\d{12}):role/(.*)(ADMIN|admin)(.*)$"\n- "^arn:aws:iam::(\\\\d{12}):role/AWSCloudFormationStackSetExecutionRole$"\n# List of tests to execute. In general the configurations follow the rules of the AWS IAM Policy Simulator.\n# For more information: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html\ntests: \n- actions: # list of actions to validate\n  - "*:*"\n  - iam:*\n  - iam:AddUser*\n  - iam:Attach*\n  - iam:Create*\n  - iam:Delete*\n  - iam:Detach*\n  - iam:Pass*\n  - iam:Put*\n  - iam:Remove*\n  - iam:UpdateAccountPasswordPolicy\n  - sts:AssumeRole\n  - sts:AssumeRoleWithSAML\n  expected_result: fail # \'fail\' or \'succeed\'\n  resources: # list of resources to validate against\n  - "*"\n  exemptions: [] # Additional exemptions (on top of the global excemptions) that will be ignored for this test\n- actions: # list of data centric actions\n  - redshift:GetClusterCredentials\n  - redshift:JoinGroup\n  - rds:Create*\n  - rds:Delete*\n  - rds:Modify*\n  - rds-db:connect\n  - s3:BypassGovernanceRetention\n  - s3:CreateBucket\n  - s3:DeleteBucket\n  - s3:DeleteBucketPolicy\n  - s3:PutBucketAcl\n  - s3:PutBucketPolicy\n  - s3:PutEncryptionConfiguration\n  - s3:ReplicateDelete\n  expected_result: fail # \'fail\' or \'succeed\'\n  resources: # list of resources to validate against\n  - "*"\n  exemptions: [\n  - "^arn:aws:iam::(\\\\d{12}):role/(.*)_worker$" # ignore this for the worker roles\n  ]\n```\n\nHowever, if you want to run positive tests (i.e. tests that you need to succeed rather than fail), these `exemptions` don\'t work that well.\n\nIn that case you can limit your tests to a set of roles and users:\n\n```yaml\n- actions:\n  - s3:PutObject\n  expected_result: succeed\n  resources:\n  - "arn:aws:s3:::my_bucket/xyz/*"\n  limit_to: # if you specify this, test will only be performed for the sources below\n  - "^arn:aws:iam::(\\\\d{12}):role/my_worker$"\n```\n\n> Note that the exemptions are ignored when using a `limit_to` list.\n\n## How to use\n\nAssuming you have define a config.yml in your local directory, then to run and write the outputs to the local `./results` directory:\n\n```bash\naws_iam_tester --write-to-file\n```\n\nUsing a specific config file:\n\n```bash\naws_iam_tester --config-file my-config.yml\n```\n\nUsing a specific output location:\n\n```bash\naws_iam_tester --output-location /tmp\n```\n\nOr write to s3:\n\n```bash\naws_iam_tester --output-location s3://my-bucket/my-prefix\n```\n\nInclude only roles that can be assumed by human beings:\n\n```bash\naws_iam_tester --no-include-system-roles\n```\n\n> Note: including system roles does NOT include the aws service roles.\n\nOr print debug output:\n\n```bash\naws_iam_tester --debug\n```\n\nTo run a limited number of evaluations (which helps speeding things up, and avoiding API throttling issues):\n\n```bash\naws_iam_tester --number-of-runs 10\n```\n\nFor more information, run `aws_iam_tester --help` for more instructions.\n',
    'author': 'Gerco Grandia',
    'author_email': 'gerco.grandia@4synergy.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gercograndia/aws-iam-tester',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
