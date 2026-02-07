# releasewatch

Send a [Pushover](https://pushover.net) notification when a new release is added to a GitHub repo

## Requirements

- Python 3.11+
- PyGithub

In addition, a Pushover application must be created and configured in the [Pushover](https://pushover.net) control panel.

## Configuration

Configuration is via environment variables:

|Config Option|Purpose|
-|-
`RELEASEWATCH_TARGET_REPOS`|comma-separated list of repo names (ex: vim/vim)
`RELEASEWATCH_GITHUB_TOKEN`|GitHub PAT token
`RELEASEWATCH_PUSHOVER_APP_KEY`|Pushover application key
`PUSHOVER_DEVICE`|Pushover device name to send notifications to
`PUSHOVER_USER_KEY`|Pushover user key

**All** configuration options are **required**.
