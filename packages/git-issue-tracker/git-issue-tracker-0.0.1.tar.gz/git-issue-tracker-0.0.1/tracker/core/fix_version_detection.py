import logging
import re

import git
from git import Repo

from tracker.core.connectors.issue_handler import IssueHandler
from tracker.core.connectors.webhook_parser import RefChangeRequest
from tracker.env import GIT_USER_PASS, MERGE_PATTERN_SEARCH_TO_SKIP, ISSUE_TRACKER_PATTERN

logger = logging.getLogger("git:repository:process")
separator = "======="


def process_hook_data(request: RefChangeRequest, handler: IssueHandler):
    try:
        committed_issues = __find_merged_commits__(request)
        handler.handle(committed_issues, request)
    except Exception as e:
        logger.error("Error has happened either on processing ref change or post hook", e)


def __find_merged_commits__(request: RefChangeRequest) -> [str]:
    r: Repo = None
    repo_path = '/tmp/tracker_{}/.git'.format(request.repo_name)
    try:
        r = git.Repo(repo_path)
    except Exception as e:
        logger.error(e)

    if r is None:
        logger.info("Cloning with GitPython over https with the username and token")
        try:
            r = git.Repo.clone_from("https://{}:{}@{}".format(
                GIT_USER_PASS["username"],
                GIT_USER_PASS["token"],
                request.repo_link.split("https://")[1]), "/tmp/tracker_{}".format(request.repo_name))
        except Exception as e:
            logger.error(e)
    logger.info("Fetch changes from remote")
    r.git.fetch()
    included_issues = set()
    commits = r.git.log('--pretty=Commit: %h%nAuthor: %ce%nDate: %ci%n%n%s%n%b%n{}'.format(separator), '{}'.format(request.to_hash[:8]),
                        '^{}'.format(request.from_hash[:8]))
    for commit_str in re.split("{}\n?".format(separator), commits):
        if re.search(MERGE_PATTERN_SEARCH_TO_SKIP, commit_str) is not None:
            logger.info("Found merge commit which skip further processing. Pattern {}".format(MERGE_PATTERN_SEARCH_TO_SKIP))
            logger.info(commit_str)
            break
        stripped_commit_msg = commit_str.strip()
        if stripped_commit_msg == '':
            continue

        logger.info("Parsed msg:\n{}".format(stripped_commit_msg))

        search = re.findall(ISSUE_TRACKER_PATTERN, commit_str)
        if len(search) > 0:
            for issue in search:
                included_issues.add(issue)

    return included_issues
