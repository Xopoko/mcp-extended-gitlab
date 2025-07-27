# GitHub Repository Setup Instructions

## Creating the Private Repository

Follow these steps to create a private GitHub repository for this project:

### 1. Create Repository on GitHub

1. Go to https://github.com/new
2. Enter repository details:
   - **Repository name**: `mcp-extended-gitlab`
   - **Description**: `Model Context Protocol server for GitLab API integration with 478+ tools`
   - **Visibility**: Select **Private**
   - **Do NOT** initialize with README, .gitignore, or license (we already have them)
3. Click **Create repository**

### 2. Push to GitHub

After creating the repository, run these commands in your terminal:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/mcp-extended-gitlab.git

# Push the code
git push -u origin master
```

If you're using SSH instead of HTTPS:
```bash
git remote add origin git@github.com:YOUR_USERNAME/mcp-extended-gitlab.git
git push -u origin master
```

### 3. Configure Repository Settings

After pushing, configure these recommended settings on GitHub:

1. **Branch Protection** (Settings → Branches):
   - Add rule for `master` branch
   - Enable "Require pull request reviews before merging"
   - Enable "Dismiss stale pull request approvals when new commits are pushed"
   - Enable "Require status checks to pass before merging"

2. **Secrets** (Settings → Secrets and variables → Actions):
   - Add `GITLAB_BASE_URL` if different from https://gitlab.com/api/v4
   - Add `GITLAB_PRIVATE_TOKEN` for testing (optional)

3. **GitHub Actions** (optional):
   Create `.github/workflows/test.yml`:
   ```yaml
   name: Test

   on: [push, pull_request]

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         - name: Install dependencies
           run: |
             pip install -r requirements-dev.txt
             pip install -e .
         - name: Run tests
           run: pytest
   ```

### 4. Invite Collaborators (if needed)

1. Go to Settings → Manage access
2. Click "Invite a collaborator"
3. Enter GitHub username or email
4. Select appropriate permission level

## Repository Structure

The repository is organized with:
- **Domain-driven architecture** in `mcp_extended_gitlab/api/`
- **Comprehensive test suite** in `tests/`
- **Development tools** for testing and code quality
- **MIT License** for open collaboration

## Next Steps

1. Set up development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   pip install -e .
   ```

2. Run tests:
   ```bash
   python run_tests.py
   ```

3. Start developing!