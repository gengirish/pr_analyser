"""Shared iteration logic for the GitHub analyzers.

Every filter walks the same gauntlet: skip unmerged PRs, parse the merge date,
and drop anything merged on or before the cutoff. ``iter_merged_after`` factors
that out so each script only has to express its own predicate.
"""

from ..common.dates import parse_timestamp


def iter_merged_after(prs, target_date):
    """Yield ``(pr, merged_at)`` for PRs merged strictly after ``target_date``.

    ``merged_at`` is returned as a parsed datetime so callers don't re-parse it.
    """
    for pr in prs:
        if not pr.get('merged_at'):
            continue
        merged_at = parse_timestamp(pr['merged_at'])
        if merged_at <= target_date:
            continue
        yield pr, merged_at
