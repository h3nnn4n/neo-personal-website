from datetime import datetime

import humanize
from django.conf import settings


def git_info(request):
    commit_time_ago = ""
    if settings.GIT_COMMIT_TIME:
        commit_dt = datetime.fromisoformat(settings.GIT_COMMIT_TIME)
        commit_time_ago = humanize.naturaltime(datetime.now(commit_dt.tzinfo) - commit_dt)

    return {
        "git_sha": settings.GIT_SHA,
        "git_commit_time_ago": commit_time_ago,
    }
