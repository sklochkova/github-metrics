import requests
from datetime import datetime, timedelta
from collections import defaultdict
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
owner = os.getenv('GITHUB_OWNER')
repo = os.getenv('GITHUB_REPO')
token = os.getenv('GITHUB_TOKEN')
start_date = os.getenv('START_DATE')
end_date = os.getenv('END_DATE')

def get_pull_requests(owner, repo, token, page=1):
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    params = {'page': page, 'state': 'closed'}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_all_pull_requests(owner, repo, token):
    all_pull_requests = []
    page = 1

    while True:
        pull_requests = get_pull_requests(owner, repo, token, page)
        
        if not pull_requests:
            break

        all_pull_requests.extend(pull_requests)
        page += 1

    return all_pull_requests

def filter_pull_requests_by_date_range(pull_requests, start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)  # Include the end date

    return [pr for pr in pull_requests if 'created_at' in pr and pr['created_at'] is not None
            and start_date <= datetime.fromisoformat(pr['created_at'].replace('Z', '')) < end_date]

def calculate_average_time(pull_requests):
    total_time_seconds = 0
    total_prs = 0

    for pr in pull_requests:
        if pr['merged_at'] is not None and pr['created_at'] is not None:
            created_at = datetime.fromisoformat(pr['created_at'].replace('Z', ''))
            merged_at = datetime.fromisoformat(pr['merged_at'].replace('Z', ''))
            total_time_seconds += (merged_at - created_at).total_seconds()
            total_prs += 1

    average_time_seconds = total_time_seconds / total_prs if total_prs > 0 else 0
    average_time_days = round(average_time_seconds / (24 * 60 * 60), 2)  # Round to two decimal points
    return average_time_seconds, average_time_days

def calculate_average_time_by_author(pull_requests):
    author_times = defaultdict(list)

    for pr in pull_requests:
        if pr['merged_at'] is not None and pr['created_at'] is not None:
            created_at = datetime.fromisoformat(pr['created_at'].replace('Z', ''))
            merged_at = datetime.fromisoformat(pr['merged_at'].replace('Z', ''))
            author = pr['user']['login']
            author_times[author].append((merged_at - created_at).total_seconds())

    mean_times_by_author = {author: sum(times) / len(times) for author, times in author_times.items()}
    return mean_times_by_author

pull_requests = get_all_pull_requests(owner, repo, token)
filtered_pull_requests = filter_pull_requests_by_date_range(pull_requests, start_date, end_date)
average_time_seconds, average_time_days = calculate_average_time(filtered_pull_requests)
average_times_by_author = calculate_average_time_by_author(filtered_pull_requests)

# Print outputs
print(f'Total average time for all pull requests from {start_date} to {end_date}:')
print(f'  - In seconds: {average_time_seconds} seconds')
print(f'  - In days: {average_time_days} days')

print("\nAverage time by author:")
for author, average_time in average_times_by_author.items():
    print(f'{author}: {average_time} seconds ({round(average_time / (24 * 60 * 60), 2)} days)')