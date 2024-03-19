"""
скрипт, который спрашивает сабреддит, парсит с него все посты за последние 3 дня
и выводит топ пользователей, которые написали больше всего комментариев и топ пользователей,
которые написали больше всего постов
"""
import time
import datetime
from collections import Counter
import praw
from praw import models


hours, minutes, seconds, mojo, bojo, dst_unknown = 0, 0, 0, 0, 0, -1
current_local_unix_time = time.time()
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


def is_subbredit_exist(name: str) -> bool:
    pass


reddit = praw.Reddit(site_name='parser_config', )


def fetch_submissions_for_period(
    subreddit: models.Subreddit, start: float, end: float,
) -> list[models.Submission]:

    submissions = []

    for submission in subreddit.new(limit=None):
        if start <= submission.created_utc <= end:
            submissions.append(submission)
            print(f'====fetch {len(submissions)} submissions in subreddit "{subreddit.title}"'
                  f' for the period from {two_days_ago_local} to {today_local}',
                  end="\r",
                  flush=True)

    print()

    return submissions


# todo что происходит с сабмишн после удаления автора?
def fetch_submissions_author_name(submissions: list[models.Submission]) -> list[str]:
    return [s.author.name for s in submissions]


def load_inner_comments(more_comment: models.MoreComments) -> str:
    for comment in more_comment.comments():
        return get_comment_author_name(comment)


def get_comment_author_name(comment: models.Comment | models.MoreComments) -> str:
    if isinstance(comment, models.MoreComments):
        return load_inner_comments(comment)

    if not comment.author:
        return 'deleted~user'

    return comment.author.name




def generate_list_of_comment_author_names(submissions: list[models.Submission]):
    return [get_comment_author_name(comment) for s in submissions
            if s.num_comments
            for comment in s.comments.list()]


def get_top_redditors(top_n: int, redditors_list: list[str]) -> list[tuple[str, int]]:
    if top_n > len(redditors_list):
        raise ValueError

    return [r for r in Counter(redditors_list).most_common(top_n)]


def get_top_commentators(top_n: int, commentators_list: list[tuple[str, int]]):
    if top_n > len(commentators_list):
        raise ValueError

    return [c for c in Counter(commentators_list).most_common(top_n)]


if __name__ == '__main__':
    subreddit = reddit.subreddit(ask_for_subreddit_name())

    # big_submission = reddit.submission('1b83npr')
    # r_test = reddit.submission('18da1zl')
    # r_tt = reddit.submission('1b8o7li')

    submissions_for_period = fetch_submissions_for_period(subreddit,
                                                          two_days_ago_local_to_unix_time,
                                                          current_local_unix_time)
    top_n = 3

    authors_of_submissions = fetch_submissions_author_name(submissions_for_period)
    top_redditors = get_top_redditors(top_n, authors_of_submissions)
    print(f'Top {top_n} redditors from {len(Counter(authors_of_submissions))}\n'
          f'\t\t{top_redditors}')


    list_of_comment_author_names = generate_list_of_comment_author_names(submissions_for_period)
    top_commentators = get_top_commentators(3, list_of_comment_author_names)
    print(f'Top {top_n} commentators from {len(Counter(list_of_comment_author_names))}\n'
          f'\t\t{top_commentators}')

    # for x in generate_list_of_comment_author_names([r_test]):
    #     print(x)

    # print(get_top_commentators(3, generate_list_of_comment_author_names([r_tt])))
