from pathlib import Path
import re
import sys

from git import Repo
from unidiff import PatchSet, PatchedFile


def is_date_line(line: str):
    pattern = re.compile(r"[-+]\s+-\s[a-zA-Z]+,\s(0?[1-9]|[12][0-9]|3[01])\s[a-zA-Z]+\s[0-9]+\s[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{1,3})?\s[a-zA-Z]+", re.IGNORECASE)
    return pattern.match(line) is not None


def only_dates_modified(patch: PatchedFile) -> bool:
    """
    Return `True` if the only lines modified in a cassette are dates.
    """
    for hunk in patch:
        n_added = sum(line.is_added for line in hunk)
        n_removed = sum(line.is_removed for line in hunk)
        if n_added != n_removed:
            return False

        return all(is_date_line(str(line)) for line in hunk if
                   line.is_added or line.is_removed)


if __name__ == '__main__':
    repo = Repo(Path(__file__).parent)
    # Get diff between HEAD and current working tree
    hcommit = repo.head.commit
    diff = repo.git.diff(None)

    patch_set = PatchSet(diff)
    responses_modified = any(not only_dates_modified(patch) for patch in patch_set)
    sys.exit(responses_modified)
