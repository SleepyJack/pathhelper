# Development Guide

This guide describes how to create, test, and promote releases for the `pathhelper` project.  
The release process is automated using GitHub Actions CI workflows for consistency and reliability.

---

## Release Types

- **Production Release:**  
  Published to **PyPI** (tag format: `vX.Y.Z`).
  
- **Test Release:**  
  Published to **TestPyPI** for pre-release testing.  
  Tag formats:  
  - Release candidate: `tX.Y.ZrcN`  
  - Development-only release: `tX.Y.ZdevN`

---

## Release Flow

For every production release (`vX.Y.Z`), at least one release candidate (`tX.Y.ZrcN`) should be published to TestPyPI first.  
This allows pre-release testing and validation before the package is made available to all users.

**Typical sequence:**

1. **Create a release candidate**  
   Tag and push:
   ```bash
   git tag t1.2.3rc1
   git push origin t1.2.3rc1
   ```
   This triggers the **Test Release CI workflow** and publishes the package to TestPyPI.

2. **Test the RC**  
   Locally, install it from TestPyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/                --extra-index-url https://pypi.org/simple                pathhelper
   ```
   Run your tests:
   ```bash
   python -m unittest discover -s tests
   ```

3. **Iterate if needed**  
   If issues are found, create and push a new RC tag:
   ```bash
   git tag t1.2.3rc2
   git push origin t1.2.3rc2
   ```

4. **Promote the RC to production**  
   Once the RC is validated, **you do not manually create the production tag**.  
   Instead, trigger the **Promote RC to Production** workflow from the GitHub Actions tab:

   - Go to: **Actions → Promote RC to Production → Run workflow**.
   - Enter the RC tag to promote (e.g., `t1.2.3rc1`).
   - Choose:
     - `dry_run: true` to validate the RC across all supported Python versions without tagging.
     - `dry_run: false` to validate and then tag.
   - The workflow will:
     1. Install the RC from TestPyPI.
     2. Run the test suite against the installed package (isolated from source tree).
     3. If all tests pass, create the production tag `vX.Y.Z` pointing to the RC commit.
   - Pushing this tag will automatically trigger the **Production Release CI workflow** and publish to PyPI.

5. **Development-only releases**  
   For experimental builds that are *not* intended as RCs, use the `dev` specifier:
   ```bash
   git tag t1.2.3dev1
   git push origin t1.2.3dev1
   ```

---

## Tagging Reference

- **Production Release:**  
  Tag format: `vX.Y.Z`  
  Example:
  ```bash
  git tag v1.2.3
  git push origin v1.2.3
  ```
  *(Normally created automatically via the promotion workflow)*

- **Release Candidate:**  
  Tag format: `tX.Y.ZrcN`  
  - `X.Y.Z` → target production version  
  - `rcN` → release candidate number (starting from 1)  
  Example:
  ```bash
  git tag t1.2.3rc1
  git push origin t1.2.3rc1
  ```

- **Development-Only Release:**  
  Tag format: `tX.Y.ZdevN`  
  - `X.Y.Z` → upcoming version you’re working toward  
  - `devN` → dev build number (starting from 1)  
  Example:
  ```bash
  git tag t1.2.3dev1
  git push origin t1.2.3dev1
  ```

---

## API Tokens

Ensure these GitHub repository secrets are set:

- `PYPI_API_TOKEN` – for production releases to PyPI.
- `TEST_PYPI_API_TOKEN` – for test releases to TestPyPI.
- `RELEASE_PROMOTION_PAT` – github PAT for release promotion workflow.
