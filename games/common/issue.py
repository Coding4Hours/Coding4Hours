from github import Github
from os import environ

def GetInfo():
    repo = Github(environ['GOD']).get_repo(environ['GITHUB_REPOSITORY'])
    issue = repo.get_issue(number=int(environ['ISSUE_NUMBER']))

    return issue, issue.user.login
