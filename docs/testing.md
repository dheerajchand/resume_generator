# Testing

The Resume Generator uses multiple testing strategies: pytest unit/integration tests, URL smoke tests, ruff linting, and vulture dead-code analysis.

---

## Running All Tests

```bash
# Run everything
make test       # pytest
make lint       # ruff
make deadcode   # vulture
make smoketest  # URL smoke tests
```

All commands run inside the Docker container.

---

## pytest (Unit and Integration Tests)

### Running

```bash
make test
```

Or directly:
```bash
make shell
pytest
```

### Configuration

Test configuration is in `pytest.ini` or `pyproject.toml` (check the project root for the active configuration file).

### Legibility Tests

The test suite includes **legibility tests** that verify generated resumes are readable and well-formatted. These tests:

1. **Generate a resume** using a known archetype and test data.
2. **Parse the output** (e.g., extract text from PDF).
3. **Assert content presence**: Verify that expected sections (name, title, experience, skills) appear in the output.
4. **Assert formatting**: Check that section headers, bullet points, and content blocks are properly structured.
5. **Assert completeness**: Verify that content from the archetype's selected items actually appears in the output.

#### What Legibility Tests Catch

- Missing sections in generated output.
- Broken template rendering.
- Content truncation bugs (data not flowing from DB to PDF).
- Encoding issues (special characters in names, titles, etc.).
- Regression in the ResumeGenerator class after code changes.

#### Example Test Structure

```python
def test_resume_contains_personal_info():
    """Generated resume should include the person's name and title."""
    data = build_test_resume_data()
    pdf_bytes = ResumeGenerator().generate(data, format="pdf", color="default_professional")
    text = extract_text_from_pdf(pdf_bytes)
    assert "Dheeraj Chand" in text
    assert "Data Scientist" in text

def test_resume_contains_positions():
    """Generated resume should include all selected positions."""
    data = build_test_resume_data()
    pdf_bytes = ResumeGenerator().generate(data, format="pdf", color="default_professional")
    text = extract_text_from_pdf(pdf_bytes)
    for position in data["positions"]:
        assert position["title"] in text
        assert position["company"] in text
```

### Writing New Tests

1. Create test files in the appropriate app directory or a top-level `tests/` directory.
2. Use `pytest` conventions: files named `test_*.py`, functions named `test_*`.
3. For tests that need database access, use Django's `@pytest.mark.django_db` decorator.
4. For tests that generate documents, consider using fixtures for test data.

---

## URL Smoke Tests

### Running

```bash
make smoketest
```

This runs the `smoke_test_urls` management command:
```bash
python manage.py smoke_test_urls
```

### What It Does

The smoke test command:

1. **Discovers all public URLs** in the application's URL configuration.
2. **Sends GET requests** to each URL using Django's test client.
3. **Asserts HTTP 200** (or other expected status codes) for each response.
4. **Reports failures** — any URL returning an unexpected status code is flagged.

### What It Catches

- Broken URL patterns (misconfigured `urls.py`).
- View function errors (import errors, missing template files).
- Database configuration issues (if views query the DB).
- Middleware problems.

### When to Run

- After changing URL configurations.
- After modifying views.
- Before deploying to production.
- As part of CI/CD pipeline.

---

## ruff (Linting)

### Running

```bash
make lint
```

Or directly:
```bash
ruff check .
```

### What It Does

[ruff](https://docs.astral.sh/ruff/) is a fast Python linter that checks for:

- **Style violations**: PEP 8 compliance, import ordering.
- **Potential bugs**: Unused variables, unreachable code, mutable default arguments.
- **Code quality**: Overly complex functions, bare excepts, f-string issues.
- **Import issues**: Unused imports, incorrect import order.

### Configuration

ruff configuration is typically in `pyproject.toml` or `ruff.toml`. Check these files for:

- Enabled rule sets (e.g., `E`, `F`, `W`, `I`).
- Ignored rules.
- Per-file overrides.
- Line length settings.

### Fixing Issues

ruff can auto-fix many issues:
```bash
ruff check --fix .
```

Review changes before committing — auto-fixes can occasionally be incorrect.

---

## vulture (Dead Code Detection)

### Running

```bash
make deadcode
```

Or directly:
```bash
vulture .
```

### What It Does

[vulture](https://github.com/jendrikseipp/vulture) finds unused Python code:

- **Unused functions**: Defined but never called.
- **Unused variables**: Assigned but never read.
- **Unused imports**: Imported but never used.
- **Unused classes**: Defined but never instantiated.
- **Unused class attributes**: Defined but never accessed.

### Understanding Output

vulture reports each finding with a confidence percentage:

```
portfolio/models.py:42: unused function 'some_function' (60% confidence)
```

Higher confidence = more likely to be genuinely unused. Lower confidence findings may be false positives (e.g., functions called dynamically, Django model methods called by the framework).

### Common False Positives

In a Django project, vulture often flags:

- **Model `Meta` classes** — Used by Django internally.
- **Admin method attributes** (e.g., `short_description`) — Used by Django admin.
- **Signal handlers** — Connected via decorators, not called directly.
- **Management command `handle()` methods** — Called by Django's command framework.
- **Migration files** — Auto-generated, not directly imported.

### Whitelist

If vulture reports persistent false positives, create a whitelist file:

```python
# vulture_whitelist.py
from portfolio.models import PersonalInfo
PersonalInfo.Meta  # Used by Django ORM
```

Then run:
```bash
vulture . vulture_whitelist.py
```

---

## Testing Strategy

### Pre-commit Checklist

Before committing code changes, run:

```bash
make lint       # Fix any style issues
make deadcode   # Review for unused code
make test       # Ensure all tests pass
make smoketest  # Verify all URLs work
```

### Pre-deploy Checklist

Before deploying to production:

1. All pre-commit checks pass.
2. Smoke tests pass against the staging/local environment.
3. Generate a resume in each format to verify rendering.
4. If email-related changes: test email sending with a test recipient.

### CI/CD Integration

These commands can be integrated into a CI pipeline:

```yaml
# Example GitHub Actions workflow
steps:
  - name: Lint
    run: make lint
  - name: Dead code check
    run: make deadcode
  - name: Tests
    run: make test
  - name: Smoke tests
    run: make smoketest
```

---

## Debugging Test Failures

### pytest failures

1. Run the failing test in isolation:
   ```bash
   pytest tests/test_specific.py::test_function_name -v
   ```
2. Add `-s` to see print output:
   ```bash
   pytest tests/test_specific.py -v -s
   ```
3. Check for database state issues — tests should be independent.

### Smoke test failures

1. Check the specific URL that failed.
2. Try accessing it manually in the browser.
3. Check for missing migrations (`make migrate`).
4. Check for missing seed data (`make loaddata`).

### Lint failures

1. Read the ruff output — it tells you exactly what rule was violated and where.
2. Use `ruff check --fix .` for auto-fixable issues.
3. For unfixable issues, update the code manually.

### Dead code findings

1. Evaluate each finding — is it genuinely unused or a false positive?
2. Remove genuinely unused code.
3. Add false positives to the whitelist.
4. Re-run to verify.
