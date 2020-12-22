from github import Github

def search_github(org_name, repo_name):
    g = Github("ACCESS-TOKEN-GOES-HERE")
    res = g.get_organization(org_name)

    for repo in res.get_repos():
        if repo.name == repo_name:
            print(f'{repo.open_issues_count}')
            break
            

if __name__ == '__main__':
    search_github("sample-org", "sample-repo")
