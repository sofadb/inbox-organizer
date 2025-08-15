# Journal File Organizer

A reusable GitHub workflow that organizes timestamped markdown files from `/inbox` into structured `/journal` directories. The workflow is published as a Docker image to GitHub Container Registry (GHCR) for better security and performance.

## Setup Instructions

### Option A: Use This Public Workflow Repository

**Recommended**: Fork this repository to get automatic updates and use the pre-built Docker image.

1. Fork this repository
2. The Docker image is automatically built and published to GHCR
3. Configure secrets (see step 2 below)

### Option B: Use the Reusable Workflow

Create a workflow in your private repository that calls this reusable workflow:

```yaml
# .github/workflows/organize-journal.yml in your private repo
name: Organize Journal Files

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:

permissions:
  contents: write

jobs:
  organize:
    uses: sofadb/inbox/.github/workflows/organize.yml@main
    with:
      image_tag: 'latest'
```

This calls the reusable workflow from `sofadb/inbox`.

### 2. Configure Secrets

**For Option A (Fork this repo):**

Create these secrets in your forked repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add secrets:
   - `PRIVATE_REPO`: Your private repository name (format: `username/repo-name`)  
   - `PRIVATE_REPO_TOKEN`: Personal Access Token with `repo` scope

**For Option B (Reusable workflow):**

Ensure your private repo has Actions enabled with write permissions:
1. **Settings** → **Actions** → **General** → **Workflow permissions**
2. Select **Read and write permissions**

### 3. Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. If Actions are disabled, click **"I understand my workflows, go ahead and enable them"**

## Architecture

This project uses a modern CI/CD approach with multiple workflows:

### 1. `build-image.yml` - Docker Image Builder
- Builds and publishes Docker image to GHCR
- Triggers on changes to `Dockerfile` or `organize_files.py`
- Multi-platform builds (AMD64/ARM64)
- Semantic versioning support

### 2. `organize.yml` - Reusable Workflow
- The main workflow that does the file organization
- Can be called from any repository
- Uses the pre-built Docker image from GHCR
- Configurable via inputs and secrets

## How It Works

### File Organization Pattern

- **Input**: Files in `/inbox` with pattern `YYYYMMDDHHMMSS.md`
- **Output**: Files moved to `/journal/YYYY/MM/DD/YYYYMMDDHHMMSS.md`

**Example:**
```
Before:
/inbox/20241225143000.md

After:
/journal/2024/12/25/20241225143000.md
```

### Default Schedule

The workflow runs automatically **daily at 2:00 AM UTC**.

## Customizing the Schedule

Edit `.github/workflows/organize-journal.yml` and modify the cron schedule:

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
```

### Common Schedule Examples

```yaml
# Every 6 hours
- cron: '0 */6 * * *'

# Twice daily (6 AM and 6 PM UTC)
- cron: '0 6,18 * * *'

# Every Monday at 9 AM UTC
- cron: '0 9 * * 1'

# Every hour
- cron: '0 * * * *'

# Every 30 minutes
- cron: '*/30 * * * *'
```

### Cron Format Reference

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * *
```

## Manual Execution

You can also run the workflow manually:

1. Go to **Actions** tab in your repository
2. Click on **"Organize Journal Files"** workflow
3. Click **"Run workflow"** button
4. Click **"Run workflow"** in the dropdown

## Testing Locally

To test the Docker container locally with your private repo:

```bash
# Clone your private repo locally
git clone https://github.com/username/your-private-repo.git test-repo

# Build the image
docker build -t file-organizer .

# Add test files to inbox
echo "# Test content" > test-repo/inbox/20241225143000.md

# Run the organizer
docker run --rm -v $(pwd)/test-repo:/data file-organizer

# Check results
ls test-repo/journal/2024/12/25/
```

## Troubleshooting

### Workflow Not Running
- Check that Actions are enabled in repository settings
- Verify the workflow file is in `.github/workflows/` directory
- Check the Actions tab for any error messages

### Permission Denied Errors
- Verify the Personal Access Token has `repo` scope
- Check that `PRIVATE_REPO` and `PRIVATE_REPO_TOKEN` secrets are correctly set
- Ensure the token hasn't expired

### Files Not Being Processed
- Verify files follow the exact pattern: `YYYYMMDDHHMMSS.md`
- Check the Actions logs for detailed error messages
- Ensure files are in the `/inbox` directory

## Workflow Logs

To view workflow execution details:
1. Go to **Actions** tab
2. Click on a workflow run
3. Click on the **"organize-files"** job to see detailed logs

## Future Improvements

The current algorithm can be enhanced by modifying `organize_files.py`:
- Add file content analysis
- Support different file types
- Add duplicate detection
- Implement custom naming schemes
- Add metadata extraction