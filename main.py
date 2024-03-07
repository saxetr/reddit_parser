"""
скрипт, который спрашивает сабреддит, парсит с него все посты за последние 3 дня и выводит топ пользователей,
которые написали больше всего комментариев и топ пользователей, которые написали больше всего постов
"""
import time
import datetime
from collections import Counter
from typing import TypeAlias
import praw
from praw import models

# https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki
# Monitor the following response headers to ensure that you're not exceeding the limits:
#
# X-Ratelimit-Used: Approximate number of requests used in this period
# X-Ratelimit-Remaining: Approximate number of requests left to use
# X-Ratelimit-Reset: Approximate number of seconds to end of period
# We enforce rate limits for those eligible for free access usage of our Data API. The limit is:
#
# 100 queries per minute (QPM) per OAuth client id
# QPM limits will be an average over a time window (currently 10 minutes) to support bursting requests.

Subreddit: TypeAlias = praw.models.Subreddit
Submission: TypeAlias = praw.models.Submission
Comment: TypeAlias = praw.models.Comment
MoreComments: TypeAlias = praw.models.MoreComments

hours, minutes, seconds, mojo, bojo, dst_unknown = 0, 0, 0, 0, 0, -1
current_unix_time = time.time()
today_local = datetime.date.today()
two_days_ago_local = today_local - datetime.timedelta(days=2)
two_days_ago_local_to_unix_time = time.mktime((two_days_ago_local.year,
                                               two_days_ago_local.month,
                                               two_days_ago_local.day,
                                               hours, minutes, seconds, mojo, bojo, dst_unknown))


def ask_for_subreddit_name() -> str:
    # is_valid = False
    # while not is_valid:
    #     user_input = input('Enter subreddit name:')
    #     validate_subreddit_name(user_input)
    return "sysadmin"


def validate_subreddit_name(name: str):
    return True


def check_is_subbredit_exist(name: str):
    pass


reddit = praw.Reddit(site_name='parser_config', )
subreddit = reddit.subreddit(ask_for_subreddit_name())

big_submission = reddit.submission('1b83npr')
r_test = reddit.submission('18da1zl')


# TODO придерживаться 100 запросов в минуту, установить счетчик и задержку
def fetch_submissions_for_period(subreddit: Subreddit, start: float, end: float) -> list[Submission]:
    return [submission for submission in subreddit.new(limit=None) if start <= submission.created_utc <= end]


def fetch_submissions_author_name(submissions):
    return [s.author.name for s in submissions]


def more_comments_handler(more_comment: MoreComments):
    for comment in more_comment.comments():
        return get_comment_author_name(comment)


def get_comment_author_name(comment) -> str:
    if isinstance(comment, MoreComments):
        return more_comments_handler(comment)
    elif not isinstance(comment.author, type(None)):  # handling deleted users
        return comment.author.name
    return 'deleted!~!user'


def generate_list_of_comment_author_names(submissions):
    for s in submissions:
        if s.num_comments:
            for comment in s.comments.list():
                # yield s.title, get_comment_author_name(comment)
                yield get_comment_author_name(comment)


def get_top_redditors(n: int, redditors_list):
    return [r for r in Counter(redditors_list).most_common(n)]


def get_top_commentators(n: int, commentators_list):
    return [c for c in Counter(commentators_list).most_common(n)]


if __name__ == '__main__':
    # print(get_top_redditors(3, fetch_submissions_author_name(
    #     fetch_submissions_for_period(subreddit, two_days_ago_local_to_unix_time, current_unix_time))))

    # print(get_top_commentators(3, generate_list_of_comment_author_names(
    #     fetch_submissions_for_period(subreddit, two_days_ago_local_to_unix_time, current_unix_time))))

    # for x in generate_list_of_comment_author_names([r_test]):
    #     print(x)

    print(get_top_commentators(3, generate_list_of_comment_author_names([r_test])))
