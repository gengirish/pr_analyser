"""Lightweight, keyword-based analysis of PR review comments."""

from collections import Counter

POSITIVE_KEYWORDS = ['good', 'great', 'nice', 'well done', 'excellent',
                     'awesome', 'perfect', 'thanks']
NEGATIVE_KEYWORDS = ['bad', 'wrong', 'incorrect', 'error', 'issue',
                     'problem', 'fix', 'bug']

THEME_KEYWORDS = {
    'code_style': ['style', 'format', 'indent', 'spacing', 'naming'],
    'performance': ['performance', 'slow', 'fast', 'optimize', 'efficient'],
    'security': ['security', 'vulnerability', 'secure', 'auth', 'permission'],
    'documentation': ['doc', 'comment', 'documentation', 'explain'],
}


def analyze_review_comments(comments):
    """Summarize a list of review comments into counts and simple sentiment."""
    users = Counter(comment['user']['login'] for comment in comments)

    comment_lengths = [len(comment['body']) for comment in comments]
    avg_comment_length = (
        sum(comment_lengths) / len(comment_lengths) if comment_lengths else 0
    )

    positive_count = 0
    negative_count = 0
    themes = {theme: 0 for theme in THEME_KEYWORDS}

    for comment in comments:
        body = comment['body'].lower()
        if any(keyword in body for keyword in POSITIVE_KEYWORDS):
            positive_count += 1
        if any(keyword in body for keyword in NEGATIVE_KEYWORDS):
            negative_count += 1
        for theme, keywords in THEME_KEYWORDS.items():
            if any(keyword in body for keyword in keywords):
                themes[theme] += 1

    return {
        'total_comments': len(comments),
        'users': dict(users.most_common()),
        'avg_comment_length': avg_comment_length,
        'sentiment': {
            'positive': positive_count,
            'negative': negative_count,
        },
        'themes': themes,
    }
