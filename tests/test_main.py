import pytest
from unittest.mock import MagicMock
import praw
from praw.models import Comment

from main import get_comment_author_name
from main import get_top_redditors


@pytest.fixture
def reddit():
    return praw.Reddit(site_name='parser_config', )


@pytest.fixture
def comment_with_empty_author(reddit):
    comment = MagicMock(Comment)
    comment.author = None
    return comment


@pytest.fixture
def comment_with_existing_author():
    comment = MagicMock(Comment)
    comment.author = MagicMock()
    comment.author.name = 'John'
    return comment


def test__get_comment_author_name__return_deleted_user(comment_with_empty_author):
    assert get_comment_author_name(comment_with_empty_author) == 'deleted~user'


def test__get_comment_author_name__return_author_name(comment_with_existing_author):
    assert get_comment_author_name(comment_with_existing_author) == 'John'


def test__get_top_redditors__when_redditors_less_than_requested_top():
    redditors = ['red', 'ditor']

    with pytest.raises(ValueError):
        top = get_top_redditors(3, redditors)