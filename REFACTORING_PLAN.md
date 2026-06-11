# Project Refactoring Plan - Modular Structure

## Current State Analysis

### Issues with Current Structure:
1. ❌ Monolithic scripts (`gitlab_mr_analyzer.py`, `convert_to_swebench.py`)
2. ❌ Duplicate code across GitHub and GitLab analyzers
3. ❌ Mixed concerns (API, parsing, formatting, output)
4. ❌ Root directory cluttered with 60+ files
5. ❌ Example scripts scattered everywhere
6. ❌ No clear separation between core logic and CLI
7. ✅ Some modular structure exists in `pr_analyzer/` but incomplete

### Existing Good Structure:
```
pr_analyzer/
├── common/          ✅ Shared utilities
├── formatters/      ✅ Output formatters
├── github/          ✅ GitHub-specific code
└── gitlab/          ✅ GitLab-specific code (partial)
```

## Proposed Modular Architecture

```
pr_analyser/
├── src/
│   └── pr_analyzer/
│       ├── __init__.py
│       ├── cli/                    # Command-line interfaces
│       │   ├── __init__.py
│       │   ├── gitlab_cli.py       # GitLab MR analyzer CLI
│       │   ├── github_cli.py       # GitHub PR analyzer CLI
│       │   └── converter_cli.py    # SWE-bench converter CLI
│       │
│       ├── core/                   # Core business logic
│       │   ├── __init__.py
│       │   ├── analyzer.py         # Base analyzer class
│       │   ├── filters.py          # Filtering logic
│       │   └── validators.py       # Validation logic
│       │
│       ├── gitlab/                 # GitLab-specific
│       │   ├── __init__.py
│       │   ├── api.py              # GitLab API client
│       │   ├── analyzer.py         # GitLab MR analyzer
│       │   └── models.py           # GitLab data models
│       │
│       ├── github/                 # GitHub-specific
│       │   ├── __init__.py
│       │   ├── api.py              # GitHub API client
│       │   ├── analyzer.py         # GitHub PR analyzer
│       │   └── models.py           # GitHub data models
│       │
│       ├── converters/             # Format converters
│       │   ├── __init__.py
│       │   ├── swebench.py         # SWE-bench converter
│       │   ├── json_converter.py   # JSON output
│       │   └── csv_converter.py    # CSV output
│       │
│       ├── formatters/             # Output formatters
│       │   ├── __init__.py
│       │   ├── text.py             # Text output
│       │   ├── html.py             # HTML reports
│       │   └── json.py             # JSON output
│       │
│       └── utils/                  # Shared utilities
│           ├── __init__.py
│           ├── dates.py            # Date utilities
│           ├── files.py            # File operations
│           ├── http.py             # HTTP utilities
│           └── logging.py          # Logging setup
│
├── scripts/                        # Convenience scripts
│   ├── gitlab/
│   │   ├── analyze_mrs.sh
│   │   ├── analyze_mrs.bat
│   │   └── convert_to_swebench.sh
│   ├── github/
│   │   ├── analyze_prs.sh
│   │   └── analyze_prs.bat
│   └── setup/
│       ├── install.sh
│       ├── install.bat
│       └── setup_tokens.sh
│
├── examples/                       # Example configurations
│   ├── gitlab_config.yaml
│   ├── github_config.yaml
│   └── swebench_config.yaml
│
├── tests/                          # Test suite
│   ├── unit/
│   │   ├── test_gitlab_api.py
│   │   ├── test_github_api.py
│   │   └── test_converters.py
│   └── integration/
│       ├── test_gitlab_analyzer.py
│       └── test_github_analyzer.py
│
├── docs/                           # Documentation
│   ├── gitlab/
│   │   ├── README.md
│   │   ├── QUICKSTART.md
│   │   └── API.md
│   ├── github/
│   │   ├── README.md
│   │   └── QUICKSTART.md
│   ├── converters/
│   │   └── SWEBENCH.md
│   └── development/
│       ├── CONTRIBUTING.md
│       └── ARCHITECTURE.md
│
├── output/                         # Output directory
│   ├── gitlab/
│   ├── github/
│   └── swebench/
│
├── .github/                        # GitHub workflows
│   └── workflows/
│       └── tests.yml
│
├── setup.py                        # Package setup
├── pyproject.toml                  # Modern Python packaging
├── requirements.txt                # Dependencies
├── requirements-dev.txt            # Dev dependencies
├── README.md                       # Main README
├── LICENSE                         # License file
└── .gitignore                      # Git ignore rules
```

## Implementation Steps

### Phase 1: Core Refactoring (Priority: HIGH)
1. ✅ Create new directory structure
2. ✅ Extract GitLab API client to `gitlab/api.py`
3. ✅ Extract GitHub API client to `github/api.py`
4. ✅ Create base analyzer class in `core/analyzer.py`
5. ✅ Move filtering logic to `core/filters.py`
6. ✅ Create data models for GitLab and GitHub

### Phase 2: CLI Separation (Priority: HIGH)
1. ✅ Create CLI entry points in `cli/`
2. ✅ Separate business logic from CLI
3. ✅ Add proper argument parsing
4. ✅ Add configuration file support

### Phase 3: Converters (Priority: MEDIUM)
1. ✅ Move SWE-bench converter to `converters/swebench.py`
2. ✅ Create base converter class
3. ✅ Add support for multiple output formats
4. ✅ Add validation for converter output

### Phase 4: Utilities & Formatters (Priority: MEDIUM)
1. ✅ Consolidate date utilities
2. ✅ Consolidate file operations
3. ✅ Improve output formatters
4. ✅ Add logging throughout

### Phase 5: Scripts & Examples (Priority: LOW)
1. ✅ Move all scripts to `scripts/` directory
2. ✅ Organize by platform (GitLab/GitHub)
3. ✅ Create example configurations
4. ✅ Add README for each script directory

### Phase 6: Documentation (Priority: MEDIUM)
1. ✅ Reorganize documentation
2. ✅ Create architecture documentation
3. ✅ Add API documentation
4. ✅ Update all READMEs

### Phase 7: Testing (Priority: HIGH)
1. ✅ Add unit tests for all modules
2. ✅ Add integration tests
3. ✅ Set up CI/CD pipeline
4. ✅ Add test coverage reporting

### Phase 8: Packaging (Priority: MEDIUM)
1. ✅ Update setup.py
2. ✅ Add pyproject.toml
3. ✅ Create proper package structure
4. ✅ Add entry points for CLI commands

## Benefits of New Structure

### 1. **Separation of Concerns**
- API logic separate from business logic
- CLI separate from core functionality
- Clear boundaries between modules

### 2. **Reusability**
- Shared utilities across GitHub and GitLab
- Base classes for common functionality
- Pluggable converters and formatters

### 3. **Maintainability**
- Easy to find and modify code
- Clear module responsibilities
- Better organization

### 4. **Testability**
- Each module can be tested independently
- Mock external dependencies easily
- Clear test structure

### 5. **Extensibility**
- Easy to add new platforms (Bitbucket, etc.)
- Easy to add new output formats
- Easy to add new converters

### 6. **Professional Structure**
- Follows Python best practices
- Standard project layout
- Easy for contributors to understand

## Migration Strategy

### Step 1: Create New Structure (No Breaking Changes)
- Create new directories
- Copy code to new locations
- Keep old files for backward compatibility

### Step 2: Update Imports
- Update all imports to use new structure
- Add deprecation warnings to old files
- Update documentation

### Step 3: Add Entry Points
- Create CLI entry points
- Add console scripts to setup.py
- Test all commands

### Step 4: Deprecate Old Files
- Add deprecation notices
- Update README with migration guide
- Keep old files for 1-2 versions

### Step 5: Remove Old Files
- Remove deprecated files
- Clean up root directory
- Final documentation update

## Timeline

- **Phase 1-2**: 2-3 days (Core refactoring + CLI)
- **Phase 3-4**: 1-2 days (Converters + Utilities)
- **Phase 5-6**: 1 day (Scripts + Documentation)
- **Phase 7-8**: 2 days (Testing + Packaging)

**Total Estimated Time**: 6-8 days

## Success Criteria

✅ All existing functionality works
✅ Code is organized in logical modules
✅ Clear separation of concerns
✅ Comprehensive test coverage (>80%)
✅ Updated documentation
✅ Easy to extend and maintain
✅ Professional project structure
