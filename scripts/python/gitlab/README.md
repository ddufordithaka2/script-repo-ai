# GitLab Repository and Pipeline Status Script

This script connects to a GitLab instance and scans a specified group to report the status of the latest pipeline and any scheduled pipelines for each project.

## Prerequisites

1.  **Python 3**: Ensure you have Python 3 installed.
2.  **python-gitlab library**: Install the required library using pip:
    ```sh
    pip install python-gitlab
    ```

## Setup

For security, the script is designed to read your GitLab URL and Private Access Token from environment variables.

1.  **Generate a Personal Access Token**:
    *   Log in to your GitLab account.
    *   Go to `User Settings` > `Access Tokens`.
    *   Create a new token with at least the `read_api` scope.
    *   Copy the token immediately. You won't be able to see it again.

2.  **Set Environment Variables**:
    Open your terminal and run the following commands, replacing the values with your GitLab instance URL and the token you just generated.

    ```sh
    export GITLAB_URL='https://gitlab.com'
    export GITLAB_PRIVATE_TOKEN='your_personal_access_token'
    ```
    *Note: If you are using a self-hosted GitLab instance, replace `https://gitlab.com` with your instance's URL.*

## How to Run

Execute the script from your terminal, providing the GitLab group name (including any parent groups) as a command-line argument.

**Example:**

```sh
python get_gitlab_repo_status.py your-gitlab-group/your-subgroup
```

The script will then connect to GitLab and print the status for each project found in that group.
