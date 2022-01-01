#!/usr/bin/env python3
import sys
from pr_checks.pull import PullRequest

from github import Github
from pydantic import BaseSettings, SecretStr, ValidationError


class ActionArgs(BaseSettings):
    repo: str
    number: int
    token: SecretStr

    class Config:
        # Github serves us action inputs as env vars like INPUT_{name}
        env_prefix = 'input_'
        case_sensitive = False


def main() -> int:
    # for ease of use with Github Actions all arguments are consumed from
    # enviornment variables instead of CLI args.
    try:
        args = ActionArgs()
    except ValidationError as e:
        print(f"error loading Settings:\n{e}")
        return 1

    gh = Github(args.token.get_secret_value())
    pr = PullRequest(gh=gh, repo=args.repo, number=args.number)
    return pr.check_and_comment()


if __name__ == '__main__':
    sys.exit(main())
