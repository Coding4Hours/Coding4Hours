""" a demonstration of my stupidity"""
from python_graphql_client import GraphqlClient
import feedparser
import pathlib
import os
import json

client = GraphqlClient(endpoint="https://api.github.com/graphql")

TOKEN = os.environ.get("GOD", "")

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


def make_query(after_cursor=None, include_organization=False):
    return GRAPHQL_SEARCH_QUERY.replace(
        "AFTER", '"{}"'.format(after_cursor) if after_cursor else "null"
    )

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
        else:
            latest_releases.append({
                "repo": repo_name,
                "release_name": "No releases found",
                "published_at": None,
                "url": None
            })

    return latest_releases

def fetch_releases(oauth_token):
    repos = []
    releases = []
    repo_names = set()
    has_next_page = True
    after_cursor = None

    while has_next_page:
        data = client.execute(
            query=make_query(after_cursor),
            headers={"Authorization": "Bearer {}".format(oauth_token)},
        )
        print()
        print(json.dumps(data, indent=4))
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
            else:
                latest_releases.append({
                    "repo": repo_name,
                    "release_name": "No releases found",
                    "published_at": None,
                    "url": None
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

releases = fetch_latest_releases()
print(releases)
releases.sort(key=lambda r: r["published_at"], reverse=True)
md = "\n".join(
  ["* [{repo} {release}]({url}) - {published_at}".format(**release)
   for release in releases[:5]]
)
readme_contents = readme.open().read()
rewritten = replace_chunk(readme_contents, "recent_releases", md)

readme.open("w").write(rewritten)

entries = fetch_blog_entries()[:5]
entries_md = "\n".join(
  ["* [{title}]({url}) - {published}".format(**entry) for entry in entries]
)
rewritten = replace_chunk(rewritten, "blog", entries_md)

readme.open("w").write(rewritten)
