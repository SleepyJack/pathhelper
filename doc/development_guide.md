
# Development Guide

This guide describes how to create and promote releases for the `pathhelper` project. The release process is automated using GitHub Actions CI workflows.

## Release Types
- **Production Release:** Published to PyPI (tag format: `vX.Y.Z`).
- **Test Release:** Published to TestPyPI for pre-release testing (tag format: `tX.Y.ZrcN` for release candidates, `tX.Y.ZdevN` for dev-only releases).

## Release Flow and Relationship

For every production release (`vX.Y.Z`), it is expected that at least one release candidate (`tX.Y.ZrcN`) is published first to TestPyPI. This allows for pre-release testing and validation before the package is made available on PyPI.

The typical flow is:
1. Create a release candidate tag (e.g., `t1.2.3rc1`) and push it. The package will be published to TestPyPI.
2. Install the release candidate from TestPyPI and run your tests locally:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pathhelper
   ```
   Then run your test suite as usual (e.g., `python -m unittest discover -s tests`).
3. If issues are found, iterate by publishing a new release candidate (e.g., `t1.2.3rc2`).
4. Once the release candidate is validated, promote it by creating a production release tag (e.g., `v1.2.3`) and pushing it. The package will be published to PyPI.
5. For development-only releases that are not intended as release candidates, use the `dev` specifier (e.g., `t1.2.3dev1`).

## Tagging a Release
- **Production Release:**
  - Tag format: `vX.Y.Z` (e.g., `v1.2.3`)
  - Example: `git tag v1.2.3 && git push origin v1.2.3`
- **Test Release:**
  - Tag format: `tX.Y.ZrcN` or `tX.Y.ZdevN` (e.g., `t1.2.3rc1`)
  - Example: `git tag t1.2.3rc1 && git push origin t1.2.3rc1`

## CI/CD Workflow
On pushing a tag, the CI workflow will:
  1. Run tests.
  2. Build the package.
  3. Validate the version format.
  4. Upload the package to PyPI (for production) or TestPyPI (for test).

## API Tokens
Ensure the following secrets are set in the GitHub repository:
  - `PYPI_API_TOKEN` (for production releases)
  - `TEST_PYPI_API_TOKEN` (for test releases)
