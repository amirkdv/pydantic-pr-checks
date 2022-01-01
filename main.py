#!/usr/bin/env python3
import sys
import argparse

from github import Github
from pydantic import BaseSettings, SecretStr, ValidationError

from pr_checks.pull import PullRequest


class ActionInputs(BaseSettings):
    repo: str
    number: int
    token: SecretStr

    class Config:
        # Github serves us action inputs as env vars like INPUT_{name}
        env_prefix = 'input_'
        case_sensitive = False


def main(args: argparse.Namespace) -> int:
    assert args.output in ['print', 'comment']

    try:
        inputs = ActionInputs()
    except ValidationError as e:
        print(f"Error loading arguments:\n{e}")
        return 1

    gh = Github(inputs.token.get_secret_value())
    pr = PullRequest(gh=gh, repo=inputs.repo, number=inputs.number)
    return pr.check(output=args.output)


if __name__ == '__main__':
    # for ease of use with Github Actions, all Github-related arguments are
    # consumed from enviornment variables instead of CLI args.
    parser = argparse.ArgumentParser(description="Run pydantic PR checks.")
    parser.add_argument('--output',
        default="print",
        help="What to do with errors: 'print' writes to stdout, 'comment' posts on Github PR"
    )
    args = parser.parse_args()

    sys.exit(main(args))
