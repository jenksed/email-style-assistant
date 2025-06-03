import pytest
from email_loader import load_user_emails

def test_load_user_emails():
    emails = load_user_emails()

    # Check that emails loaded is a list
    assert isinstance(emails, list), "Expected list of emails"

    # Check the first email has expected keys
    assert "subject" in emails[0], "Email should have 'subject'"
    assert "body" in emails[0], "Email should have 'body'"
    assert "tags" in emails[0], "Email should have 'tags'"

    # Check tags is a list
    assert isinstance(emails[0]["tags"], list), "'tags' should be a list"

    # Optionally check for non-empty values
    assert emails[0]["subject"] != "", "Subject should not be empty"
    assert emails[0]["body"] != "", "Body should not be empty"
    assert len(emails) > 0, "There should be at least one email loaded"
