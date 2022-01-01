from typing import List
from ..pull import PullRequest


class MockObject(object):
    """Creates a bare python object with specified attributes/methods bound to it."""
    def __init__(self, **attrs):
        super().__init__()
        for k, v in attrs.items():
            setattr(self, k, v)


def mock_pr(
    author: str = 'user',
    title: str = 'Title',
    body: str = '## Change Summary\n\n## Related issue number\n\n## Checklist',
    files: List[str] = ['changes/123-user.md']
) -> PullRequest:
    pr = MockObject(
        body=body,
        title=title,
        user=MockObject(login=author),
        get_files=lambda: [MockObject(filename=f) for f in files],
    )
    repo = MockObject(get_pull=lambda _: pr)
    gh = MockObject(get_repo=lambda _: repo)
    return PullRequest(gh=gh, repo=':mock:/:repo:', number=1)
