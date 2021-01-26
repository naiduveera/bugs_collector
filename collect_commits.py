from github import Github
import csv
import sys
import getopt
import os


def search_github(full_repo_name):
    org_name = full_repo_name.split('/')[0]
    repo_name = full_repo_name.split('/')[1]
    repo_object = None

    commit_summary_file = f'{org_name}-{repo_name}-commits'

    commits_object = None
    g = Github("bd71ca67d51f9fa6f0280c008b480b76e3bb1e81")
    res = g.get_organization(org_name)

    for repo in res.get_repos():
        if repo.name == repo_name:
            commits_object = repo.get_commits()
            repo_object = repo
            break

    if os.path.exists(f'{commit_summary_file}.csv'):
        commit_summary_file = f'{commit_summary_file}-duplicate'

    i = 0

    with open(f'{commit_summary_file}.csv', mode='a', newline='', encoding='utf-8') as csv_file:
        commit_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        commit_writer.writerow(["PULL_REQUEST_ID", "COMMIT_SHA", "FILENAME", "COMMIT URL"])
        for commitItem in commits_object:
            if i > 10:
                break
            for file in commitItem.files:
                commit_writer.writerow([commitItem.me, commitItem.sha, file.filename,commitItem.html_url])
            i = i+1

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
