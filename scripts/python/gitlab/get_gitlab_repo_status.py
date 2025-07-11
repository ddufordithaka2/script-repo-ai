import gitlab
import argparse
import os

def get_repo_and_pipeline_status(gitlab_url, private_token, group_name):
    """
    Connects to GitLab, iterates through all projects in a group,
    and prints the status of the latest pipeline and any scheduled pipelines.

    Args:
        gitlab_url (str): The URL of your GitLab instance (e.g., 'https://gitlab.com').
        private_token (str): Your GitLab private access token.
        group_name (str): The name (path) of the GitLab group to scan.
    """
    print(f"Connecting to {gitlab_url}...")
    try:
        gl = gitlab.Gitlab(gitlab_url, private_token=private_token)
        gl.auth()
        print("Authentication successful.")
    except Exception as e:
        print(f"Failed to connect or authenticate: {e}")
        return

    try:
        group = gl.groups.get(group_name)
        print(f"\nFound group: '{group.name}'. Iterating through projects...")
        print("==================================================")
    except gitlab.exceptions.GitlabGetError:
        print(f"Error: Group '{group_name}' not found. Please check the group name.")
        return

    projects = group.projects.list(all=True, include_subgroups=True)

    if not projects:
        print("No projects found in this group.")
        return

    for project in projects:
        print(f"\n--- Project: {project.name_with_namespace} ---")

        # Get the latest pipeline status for the default branch
        try:
            # Fetch the full project object to get the default branch
            p = gl.projects.get(project.id)
            pipelines = p.pipelines.list(ref=p.default_branch, get_all=False)
            if pipelines:
                latest_pipeline = pipelines[0]
                print(f"  -> Latest pipeline on '{p.default_branch}' branch: Status = {latest_pipeline.status}")
            else:
                print(f"  -> No pipelines found for the default branch ('{p.default_branch}').")
        except Exception as e:
            print(f"  -> Could not retrieve pipeline status: {e}")

        # Get scheduled pipelines
        try:
            schedules = p.pipelineschedules.list(get_all=True)
            if schedules:
                print("  -> Scheduled Pipelines:")
                for schedule in schedules:
                    status = "active" if schedule.active else "inactive"
                    print(f"    - Description: '{schedule.description}'")
                    print(f"      Cron: '{schedule.cron}' | Target: '{schedule.ref}' | Status: {status}")
            else:
                print("  -> No scheduled pipelines found.")
        except Exception as e:
            print(f"  -> Could not retrieve scheduled pipelines: {e}")

if __name__ == "__main__":
    # --- Configuration ---
    # Option 1: Set environment variables (recommended)
    # export GITLAB_URL='https://gitlab.com'
    # export GITLAB_PRIVATE_TOKEN='your_token_here'
    GITLAB_URL = os.getenv('GITLAB_URL', 'https://gitlab.com') # Default to public GitLab
    GITLAB_PRIVATE_TOKEN = os.getenv('GITLAB_PRIVATE_TOKEN')

    # Option 2: Hardcode your details here (less secure)
    # GITLAB_URL = "https://your.gitlab.instance.com"
    # GITLAB_PRIVATE_TOKEN = "your_private_token"

    parser = argparse.ArgumentParser(
        description="Get the status of all repositories and scheduled pipelines in a GitLab group.",
        epilog="Example: python get_gitlab_repo_status.py my-gitlab-group"
    )
    parser.add_argument("group_name", help="The name/path of the GitLab group to scan (e.g., 'my-org/my-team').")
    args = parser.parse_args()

    if not GITLAB_PRIVATE_TOKEN:
        print("Error: GITLAB_PRIVATE_TOKEN environment variable not set.")
        print("Please set the environment variable or hardcode the token in the script.")
    else:
        get_repo_and_pipeline_status(GITLAB_URL, GITLAB_PRIVATE_TOKEN, args.group_name)
