# tests/test_app_logic.py

import pytest
from app import filter_emails_by_tags

mock_emails = [
    {"subject": "Email A", "tags": ["work", "project"]},
    {"subject": "Email B", "tags": ["family"]},
    {"subject": "Email C", "tags": ["project", "urgent"]}
]

def test_filter_with_matching_tag():
    filtered = filter_emails_by_tags(mock_emails, ["project"])
    assert len(filtered) == 2

def test_filter_with_no_tags_selected():
    filtered = filter_emails_by_tags(mock_emails, [])
    assert len(filtered) == 3

def test_filter_with_no_matches():
    filtered = filter_emails_by_tags(mock_emails, ["vacation"])
    assert len(filtered) == 0
