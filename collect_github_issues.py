from github import Github

def search_github(org_name, repo_name):
    g = Github("ACCESS-TOKEN-GOES-HERE")
    res = g.get_organization(org_name)

    #Will be refactored to check each page.
    for repo in res.get_repos():
        if repo.name == "elasticsearch":
            issues_object = repo.get_issues()
            break

    with open('issues.csv', mode='w') as csv_file:
        issue_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for issue in issues_object:
            issue_writer.writerow([issue.id, issue.title, issue.state, issue.created_at, issue.html_url])


            

if __name__ == '__main__':
    search_github("sample-org", "sample-repo")
