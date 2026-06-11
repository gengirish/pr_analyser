from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="github-pr-analyzer",
    version="0.1.0",
    author="GitHub PR Analyzer Team",
    author_email="example@example.com",
    description="A tool to analyze GitHub PRs with specific criteria",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/github-pr-analyzer",
    packages=find_packages(),
    py_modules=["github_pr_analyzer"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "python-dateutil>=2.8.1",
    ],
    entry_points={
        "console_scripts": [
            "github-pr-analyzer=github_pr_analyzer:main",
        ],
    },
)
