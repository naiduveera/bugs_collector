from github import Github
import csv
import sys
import getopt
import os
import random


def get_buggy_files(repo, pull_request):
    files_list = []
    pull_request_id = int(pull_request.html_url.split("/")[-1])
    github_files = (repo.get_pull(pull_request_id)).get_files()

    for github_file in github_files:
        files_list.append(github_file.filename)

    return files_list


def search_github(full_repo_name):
    org_name = full_repo_name.split('/')[0]
    repo_name = full_repo_name.split('/')[1]
    repo_object = None

    issue_summary_file = f'{org_name}-{repo_name}'

    issues_object = None
    g = Github(os.getenv('GITHUB_ACCESS_TOKEN'))
    res = g.get_organization(org_name)

    for repo in res.get_repos():
        if repo.name == repo_name:
            issues_object = repo.get_issues(state='all')
            repo_object = repo
            break

    if os.path.exists(f'{issue_summary_file}.csv'):
        issue_summary_file = f'{issue_summary_file}-duplicate'

    with open(f'{issue_summary_file}.csv', mode='a', newline='', encoding='utf-8') as csv_file:
        issue_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        issue_writer.writerow(["ISSUE ID", "ISSUE_TITLE", "FILES", "ISSUE STATE", "ISSUE CREATED AT", "ISSUE URL"])
        for issue in issues_object:
            for label in issue.labels:
                if label.name == "bug":
                    if issue.labels:
                        if issue.pull_request:
                            buggy_files = get_buggy_files(repo_object, issue.pull_request)
                            for file_name in buggy_files:
                                issue_writer.writerow(
                                    [issue.id, issue.title, file_name, issue.state, issue.created_at, issue.html_url])


def evaluate_args():
    argument_list = sys.argv[1:]
    short_options = "hr:"
    long_options = ["help", "repository="]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)
    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print("Usage: get_github_issues.py -r <organization/repository>")
        elif current_argument in ("-r", "--repository"):
            return current_value


if __name__ == '__main__':
    git_repo = evaluate_args()
    if git_repo:
        search_github(git_repo)
