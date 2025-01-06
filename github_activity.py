import sys
import urllib.request
import json

def fetch_github_activity(username):
    """
    Fetch recent activity for a given GitHub username using the GitHub API.

    :param username: GitHub username
    :return: List of activities or an error message
    """
    api_url = f"https://api.github.com/users/{username}/events"

    try:
        # Make the HTTP request
        with urllib.request.urlopen(api_url) as response:
            if response.status != 200:
                return f"Error: Received status code {response.status} from GitHub API."

            # Parse the JSON response
            data = json.loads(response.read().decode('utf-8'))

            # Extract and format activities
            activities = []
            for event in data:
                event_type = event.get('type')
                repo_name = event['repo']['name'] if 'repo' in event else "unknown"

                if event_type == 'PushEvent':
                    commit_count = len(event['payload']['commits'])
                    activities.append(f"Pushed {commit_count} commits to {repo_name}")
                elif event_type == 'IssuesEvent':
                    action = event['payload']['action']
                    activities.append(f"{action.capitalize()} a new issue in {repo_name}")
                elif event_type == 'WatchEvent':
                    activities.append(f"Starred {repo_name}")
                elif event_type == 'ForkEvent':
                    activities.append(f"Forked {repo_name}")
                else:
                    activities.append(f"Performed {event_type} on {repo_name}")

            return activities if activities else ["No recent activity found."]

    except urllib.error.HTTPError as e:
        return [f"HTTP Error: {e.code} - {e.reason}"]
    except urllib.error.URLError as e:
        return [f"URL Error: {e.reason}"]
    except Exception as e:
        return [f"An unexpected error occurred: {str(e)}"]

if __name__ == "__main__":
    # Ensure a username is provided
    if len(sys.argv) != 2:
        print("Usage: github-activity <username>")
        sys.exit(1)

    username = sys.argv[1]
    activities = fetch_github_activity(username)

    # Display the activity
    if isinstance(activities, list):
        for activity in activities:
            print(f"- {activity}")
    else:
        print(activities)
