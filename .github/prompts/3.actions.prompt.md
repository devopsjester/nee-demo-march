# GitHub Actions Workflow for Weather CLI App

## Objective
Create a GitHub Actions workflow to automate the building, testing, packaging, and releasing of the "weather" Python CLI application to GitHub Packages.

## Workflow File
- Create a new YAML file named `python-publish.yml` in the `.github/workflows/` directory.

## Workflow Triggers
- The workflow should trigger on:
    - Pushes to the `main` branch.
    - Creation of tags matching the pattern `v*.*.*` (e.g., `v1.0.0`, `v0.1.2`).
    - Manually, via `workflow_dispatch`.

## Workflow Jobs

### 1. `build-and-test` Job
   - **Runner:** Use `ubuntu-latest`.
   - **Steps:**
     - **Checkout Code:** Use `actions/checkout@v4`.
     - **Set up Python:**
       - Use `actions/setup-python@v5`.
       - Specify a matrix of Python versions to test against: `3.9`, `3.10`, `3.11`.
     - **Install Dependencies:**
       - Command: `python -m pip install --upgrade pip`
       - Command: `python -m pip install -r requirements.txt`
       - Include any build/packaging dependencies like `setuptools`, `wheel`, and `twine` in `requirements.txt` if they are not already there.
     - **Run Linters/Formatters (Optional but Recommended):**
       - If tools like Flake8 or Black are used, add a step to run them.
       - Example: `flake8 .`
     - **Run Tests:**
       - Command: `pytest`
     - **Build Package:**
       - Command: `python setup.py sdist bdist_wheel`
     - **Upload Artifacts (Wheels and Source Distribution):**
       - Use `actions/upload-artifact@v4`.
       - Upload the contents of the `dist` directory.

### 2. `publish-to-github-packages` Job
   - **Runner:** Use `ubuntu-latest`.
   - **Needs:** This job should depend on the successful completion of the `build-and-test` job (`needs: build-and-test`).
   - **Condition:** Only run this job if the trigger is a tag matching `v*.*.*`.
     - `if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v')`
   - **Permissions:**
     - `contents: read`
     - `packages: write`
   - **Steps:**
     - **Checkout Code:** Use `actions/checkout@v4` (if needed, or download artifacts).
     - **Download Build Artifacts:**
       - Use `actions/download-artifact@v4` to download the artifacts uploaded by the `build-and-test` job.
     - **Set up Python:**
       - Use `actions/setup-python@v5` (e.g., Python 3.9).
     - **Install Publishing Tools:**
       - Command: `python -m pip install --upgrade pip`
       - Command: `python -m pip install twine` (ensure `twine` is in `requirements.txt` or install it explicitly here).
     - **Publish to GitHub Packages:**
       - Use `twine upload`.
       - Target repository URL: `https://upload.pypi.org/legacy/` (This is the standard PyPI URL, for GitHub Packages it's different. The prompt should guide towards GitHub Packages specifically).
       - **Correction for GitHub Packages:**
         - The `twine upload` command should be configured to publish to GitHub Packages.
         - Environment variables for `TWINE_USERNAME` (should be `__token__`) and `TWINE_PASSWORD` (should be `${{ secrets.GITHUB_TOKEN }}`).
         - The repository URL for `twine` should be `https://pypi.pkg.github.com/YOUR_USERNAME_OR_ORG/` (The prompt should instruct to replace `YOUR_USERNAME_OR_ORG` or use a dynamic variable like `${{ github.repository_owner }}`).
         - Command: `python -m twine upload --repository-url https://pypi.pkg.github.com/${{ github.repository_owner }} dist/*` (or the path to the downloaded artifacts).
           - *Self-correction: The above URL is for PyPI-like hosting on GitHub Packages. For Python packages, it's usually `https://pypi.pkg.github.com/{OWNER}`. The command should be `python -m twine upload --repository-url https://pypi.pkg.github.com/${{ github.repository_owner }}/ dist/*` if the package name doesn't include the repo name, or just target the `dist/*` files with correct `TWINE_REPOSITORY_URL` env var.*
         - **Revised Command for GitHub Packages:**
           `TWINE_USERNAME: __token__`
           `TWINE_PASSWORD: ${{ secrets.GITHUB_TOKEN }}`
           `TWINE_REPOSITORY_URL: https://pypi.pkg.github.com/${{ github.repository_owner }}`
           `python -m twine upload dist/*` (assuming artifacts are in `dist/`)

## Dependencies Update
- Ensure `setuptools`, `wheel`, and `twine` are added to `requirements.txt`.
- After updating `requirements.txt`, run `python3 -m pip install -r requirements.txt` locally to confirm.

## README Update
- Add a section to the `README.md` explaining:
    - That the project uses GitHub Actions for CI/CD.
    - How to view the build and test status (e.g., by adding a workflow status badge).
    - How releases are published to GitHub Packages.
- Example Status Badge:
  `[![CI/CD](https://github.com/<OWNER>/<REPO>/actions/workflows/python-publish.yml/badge.svg)](https://github.com/<OWNER>/<REPO>/actions/workflows/python-publish.yml)`
  (Instruct to replace `<OWNER>` and `<REPO>`).

## Security
- The `GITHUB_TOKEN` used for publishing has limited permissions by default. Ensure the `permissions` block in the `publish-to-github-packages` job is correctly set for `packages: write`.