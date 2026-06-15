```markdown
# CivicLens Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches the core development patterns used in the CivicLens repository, a Python codebase with no detected framework. It covers file naming, import/export styles, commit patterns, and testing conventions. The guide is designed to help contributors maintain consistency and efficiency when working on CivicLens.

## Coding Conventions

### File Naming
- Use **camelCase** for file names.
  - **Example:** `userProfile.py`, `dataFetcher.py`

### Import Style
- Use **relative imports** within the codebase.
  - **Example:**
    ```python
    from .utils import parseData
    from ..models import User
    ```

### Export Style
- Use **named exports** (explicitly define what is exported from a module).
  - **Example:**
    ```python
    def processData(data):
        # processing logic
        return result

    __all__ = ['processData']
    ```

### Commit Patterns
- Commit messages are **freeform** (no strict prefix), with an average length of 51 characters.
  - **Example:**  
    `Fix bug in data parsing for user uploads`

## Workflows

_No automated workflows detected in the repository._

## Testing Patterns

- **Testing Framework:** Unknown (not specified in the codebase)
- **Test File Pattern:** Test files are named using the `*.test.*` pattern.
  - **Example:** `userProfile.test.py`, `dataFetcher.test.py`
- **Writing Tests:** Place test files alongside the code they test, following the naming pattern.

## Commands
| Command | Purpose |
|---------|---------|
| /new-file | Create a new Python file using camelCase naming |
| /import-relative | Insert a relative import statement |
| /export-named | Add named exports to a module |
| /write-test | Generate a test file with the *.test.* pattern |
| /commit-guidance | Show commit message best practices |
```
