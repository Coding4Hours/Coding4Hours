""" a demonstration of my stupidity"""
from python_graphql_client import GraphqlClient
import feedparser
import pathlib
import os
import json
import requests
import re

client = GraphqlClient(endpoint="https://api.github.com/graphql")

TOKEN = os.environ.get("GOD", "")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

GRAPHQL_SEARCH_QUERY = """
query {
  search(first: 100, type:REPOSITORY, query:"is:public owner:coding4hours sort:updated", after: AFTER) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      __typename
      ... on Repository {
        name
        description
        url
        releases(orderBy: {field: CREATED_AT, direction: DESC}, first: 1) {
          totalCount
          nodes {
            name
            publishedAt
            url
          }
        }
      }
    }
  }
}
"""


def replace_chunk(content, marker, chunk):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

def fetch_latest_releases():
    query = """
    query($user: String!, $repo_count: Int!) {
        user(login: $user) {
            repositories(first: $repo_count, orderBy: {field: CREATED_AT, direction: DESC}) {
                nodes {
                    name
                    releases(last: 1) {
                        nodes {
                            name
                            publishedAt
                            url
                        }
                    }
                }
            }
        }
    }
    """
    variables = {"user": "coding4hours", "repo_count": 100}
    url = "https://api.github.com/graphql"
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=HEADERS)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}, {response.text}")
    
    data = response.json()
    repos = data['data']['user']['repositories']['nodes']
    latest_releases = []

    for repo in repos:
        repo_name = repo['name']
        if repo['releases']['nodes']:
            latest_release = repo['releases']['nodes'][0]
            latest_releases.append({
                "repo": repo_name,
                "release_name": latest_release['name'],
                "published_at": latest_release['publishedAt'],
                "url": latest_release['url']
            })

    return latest_releases


def fetch_blog_entries():
    entries = feedparser.parse("https://coding4hours.github.io/feed.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]


root = pathlib.Path(__file__).parent.resolve()

readme = root / "README.md"
#project_releases = root / "RELEASES.md"

#releases = fetch_latest_releases()
#project_releases_md = "\n".join(
#  [
#    (
#      "* **[{repo}]({repo_url})**: [{release}]({url}) {total_releases_md}- {published_day}\n"
#      "<br />{description}")
#    .format(
#      total_releases_md="- ([{} releases total]({}/releases)) ".format(
#        release["total_releases"], release["repo_url"]
#      )
#      if release["total_releases"] > 1
#      else "",
#      **release
#    )
#    for release in releases
#  ]
#)

#project_releases_content = project_releases.open().read()
#project_releases_content = replace_chunk(
#  project_releases_content, "recent_releases", project_releases_md
#)
#project_releases_content = replace_chunk(
#  project_releases_content, "project_count", str(len(releases)), inline=True
#)
#project_releases_content = replace_chunk(
#  project_releases_content,
#  "releases_count",
#  str(sum(r["total_releases"] for r in releases)),
#  inline=True,
#)
#poject_releases.open("w").write(project_releases_content)

entries = fetch_blog_entries()[:5]
entries_md = "\n".join(
  ["* [{title}]({url}) - {published}".format(**entry) for entry in entries]
)
rewritten = replace_chunk(rewritten, "blog", entries_md)

readme.open("w").write(rewritten)
