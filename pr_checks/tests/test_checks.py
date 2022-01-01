from .mocks import mock_pr
from textwrap import dedent


def test_check_sanity():
    pr = mock_pr()
    errors = pr.check_all()
    assert len(errors) == 0


def test_check_ids_in_title():
    pr = mock_pr(title='Lorem #123 ipsum')
    assert pr.check_ids_in_title() is not None

    pr = mock_pr(title='Lorem ipsum #123')
    assert pr.check_ids_in_title() is not None

    pr = mock_pr(title='Lorem ipsum 123')
    assert pr.check_ids_in_title() is None


def test_check_change_summary():
    pr = mock_pr(body=dedent("""
    ## Change Summary

    """))
    assert pr.check_change_summary() is None

    pr = mock_pr(body=dedent("""
    ## Summary of Changes

    """))
    assert pr.check_change_summary() is not None


def test_check_related_issue_ref():
    pr = mock_pr(body="## Related issue number")
    assert pr.check_related_issue_ref() is None

    pr = mock_pr(body=dedent("""
    ## Related issue number

    Ok to not reference any issues.
    """))
    assert pr.check_related_issue_ref() is None

    pr = mock_pr(body=dedent("""
    ## Related issue number

    If referecing the verb must be valid like fixes #123.
    """))
    assert pr.check_related_issue_ref() is None

    pr = mock_pr(body=dedent("""
    ## Related issue number

    Arbitrary verbs #123 not allowed
    """))
    assert pr.check_related_issue_ref() is not None


def test_check_checklist():
    pr = mock_pr(body=dedent("""
    ## Checklist

    * [x] done
    """))
    assert pr.check_checklist() is None

    pr = mock_pr(body=dedent("""
    ## Checklist

    * [ ] not done
    """))
    assert pr.check_checklist() is not None


def test_changes_md():
    pr = mock_pr(files=['foo.py', 'changes/100-alice.md'], author='alice')
    assert pr.check_changes_md_file() is None

    pr = mock_pr(files=['foo.py'])
    assert pr.check_changes_md_file() is not None

    pr = mock_pr(files=['foo.py', 'changes/100-alice.md'], author='bob')
    assert pr.check_changes_md_file() is not None
