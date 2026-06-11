"""Console + file output helpers."""

import datetime

SEPARATOR = '-' * 80


class OutputWriter:
    """Write messages to the console and, optionally, to a file.

    Replaces the ``print_output`` closure that was duplicated in the GitHub and
    GitLab analyzers. When no filename is given a timestamped default is used.
    """

    def __init__(self, filename=None, default_prefix='pr_results', encoding='utf-8'):
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{default_prefix}_{timestamp}.txt"
        self.filename = filename
        try:
            self._file = open(filename, 'w', encoding=encoding)
            print(f"Results will be saved to {filename}")
        except OSError as exc:
            self._file = None
            print(f"Error opening output file: {exc}")
            print("Results will only be displayed on screen")

    def write(self, message=''):
        """Print a line to the console and to the file (if open)."""
        print(message)
        if self._file:
            print(message, file=self._file)

    def separator(self):
        self.write(SEPARATOR)

    def close(self):
        if self._file:
            self._file.close()
            print(f"Results have been saved to {self.filename}")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False
