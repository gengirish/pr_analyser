"""File-path classification shared across the GitHub and GitLab analyzers.

Every analyzer needs to answer the same questions about a changed file: is it a
test, is it "real" source code, does it match a requested extension or
directory? Those rules used to be copy-pasted into a dozen scripts; they now
live here.
"""

# Source-code extensions treated as "real code" by the GitHub analyzers.
SOURCE_EXTENSIONS = (
    '.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.go',
    '.rb', '.php', '.ts', '.swift',
)

# The GitLab analyzer historically recognized a couple of extra JVM languages.
SOURCE_EXTENSIONS_EXTENDED = SOURCE_EXTENSIONS + ('.kt', '.scala')

# Substrings that mark a file as documentation/config rather than source code.
DOC_EXCLUDES = ('readme', 'license', 'changelog', 'docs/', 'doc/', 'example')


def is_test_file(path):
    """Return True if the path looks like a test or spec file."""
    name = path.lower()
    return 'test' in name or 'spec' in name


def is_source_file(path, extensions=SOURCE_EXTENSIONS):
    """Return True if the path is source code (and not docs/config)."""
    name = path.lower()
    return name.endswith(extensions) and not any(x in name for x in DOC_EXCLUDES)


def classify_files(paths, extensions=SOURCE_EXTENSIONS):
    """Split an iterable of file paths into (test_files, source_files).

    A path that is neither a test nor a recognized source file is ignored,
    matching the behavior of the original analyzers.
    """
    test_files = []
    source_files = []
    for path in paths:
        if is_test_file(path):
            test_files.append(path)
        elif is_source_file(path, extensions):
            source_files.append(path)
    return test_files, source_files


def normalize_extensions(raw):
    """Turn a comma string like 'py,.js' into ['.py', '.js']."""
    types = [t.strip().lower() for t in raw.split(',') if t.strip()]
    return [t if t.startswith('.') else f'.{t}' for t in types]


def normalize_directories(raw):
    """Turn a comma string like '/src,docs' into ['src/', 'docs/'] prefixes."""
    directories = []
    for directory in (d.strip() for d in raw.split(',') if d.strip()):
        if directory.startswith('/'):
            directory = directory[1:]
        if not directory.endswith('/'):
            directory = directory + '/'
        directories.append(directory)
    return directories


def matches_extension(path, extensions):
    """Return True if path ends with any of the (dot-prefixed) extensions."""
    name = path.lower()
    return any(name.endswith(ext) for ext in extensions)


def matches_directory(path, directories):
    """Return True if path starts with any of the (slash-suffixed) directories."""
    return any(path.startswith(directory) for directory in directories)
