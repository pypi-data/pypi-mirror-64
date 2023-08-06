import json
from functools import reduce
import operator
from typing import Iterable, Any, List, Tuple, Set
from collections import Counter
import logging
import re


def load_data(path: str) -> list:
    return json.load(open(path, 'r', encoding='utf8'))


def get_by_path(root: dict, items: Iterable) -> Any:
    # courtesy: https://stackoverflow.com/a/14692747/5538961
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def get_issue_type(issue: dict) -> str:
    return get_by_path(issue, ('fields', 'issuetype', 'name'))


def get_reference(issue):
    return issue['key']


def get_title(issue):
    return get_by_path(issue, ('fields', 'summary'))


def get_labels(issue) -> list:
    return get_by_path(issue, ('fields', 'labels'))


def get_description(issue):
    return get_by_path(issue, ('fields', 'description'))


def get_status(issue) -> str:
    return get_by_path(issue, ('fields', 'status', 'name'))


def get_priority(issue) -> str:
    return get_by_path(issue, ('fields', 'priority', 'name'))


def get_date_created(issue) -> str:
    return get_by_path(issue, ('fields', 'created'))


def get_date_updated(issue) -> str:
    return get_by_path(issue, ('fields', 'updated'))


def get_issue_owner(issue: dict) -> str:
    """try to retrieve the displayName, when it failed return an empty str"""
    try:
        return get_by_path(issue, ('fields', 'assignee', 'displayName'))
    except TypeError:
        logging.warning(
            f'not able to retrieve assignee name from "{issue["key"]}", is there an assignee ?')
        return ''


def filter_epics(issues: list) -> list:
    return [issue for issue in issues if get_issue_type(issue) == 'Epic']


def struct_comment(comment: dict, size_limit: int) -> tuple:
    """retrieve key information :(author,comment content)"""
    def normalize(text):
        if not text:
            return
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        return text
    text = comment['body']
    author = comment['author']
    if author.get('displayName'):
        name = author['displayName']
    else:
        name = author['key']
    text = normalize(text) if len(text) < size_limit else 'too long'
    return (name, text)


def get_comments(issue: dict) -> dict:
    """retrieve information regarding last comment for an issue"""
    comments = get_by_path(issue, ('fields', 'comment', 'comments'))
    if len(comments) == 0:
        return {}
    last_comment = comments[-1]
    return {'ref': get_reference(issue),
            'comment': struct_comment(last_comment, 450),
            'comment_update': last_comment['updated']
            }


def get_jiradata(issue: dict) -> dict:
    return {
        'ref': get_reference(issue),
        'status': get_status(issue),
        'priority': get_priority(issue),
        'issue_type': get_issue_type(issue),
        'date_update': get_date_updated(issue),
        'date_created': get_date_created(issue),
        'title': get_title(issue),
        'description': get_description(issue),
        'labels': get_labels(issue),
        'owner': get_issue_owner(issue)
    }


def get_top_label(issues) -> Set[Tuple[str, float]]:
    """retrieve top tags and compute relative usage normalize between 0,1"""
    labels = [get_labels(issue) for issue in issues]
    all_labels = reduce(operator.add, labels)
    counter = Counter(all_labels)
    nb_ticket = len(issues)
    return set((k, round(v/nb_ticket, 2)) for k, v in counter.most_common())
