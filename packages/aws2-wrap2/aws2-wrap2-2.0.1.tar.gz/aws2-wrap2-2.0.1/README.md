# Attention!

This package is fork of [linaro\-its/aws2\-wrap: Simple script to export current AWS SSO credentials or run a sub\-process with them](https://github.com/linaro-its/aws2-wrap).
If [Improve argument handling by bigwheel · Pull Request \#13 · linaro\-its/aws2\-wrap](https://github.com/linaro-its/aws2-wrap/pull/13) is merged,
this package will be disposed.

# aws2-wrap2
This is a simple script to facilitate exporting the current AWS SSO credentials or runing a command with them. Please note that it is called `aws2-wrap2` to show that it works with AWS CLI v2, even though the CLI tool is no longer called `aws2`.

## Install using `pip`

https://pypi.org/project/aws2-wrap2

`pip install aws2-wrap2==2.0.1`

## Run a command using AWS SSO credentials

`aws2-wrap2 [--profile <awsprofilename>] <command>`

For example:

`aws2-wrap2 --profile MySSOProfile terraform plan`

## Export the credentials

There may be circumstances when it is easier/better to set the appropriate environment variables so that they can be re-used by any `aws` command.

Since the script cannot directly set the environment variables in the calling shell process, it is necessary to use the following syntax:

`eval "$(aws2-wrap2 [--profile <awsprofilename>] --export)"`

For example:

`eval "$(aws2-wrap2 --profile MySSOProfile --export)"`
