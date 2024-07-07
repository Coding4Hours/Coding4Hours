""" a demonstration of my stupidity"""
from python_graphql_client import GraphqlClient
import feedparser
import pathlib
import os

client = GraphqlClient(endpoint="https://api.github.com/graphql")

TOKEN = os.environ.get("GOD", "")


def replace_chunk(content, marker, chunk):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


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
        print()
        for repo in data["data"]["viewer"]["repositories"]["nodes"]:
            if repo["releases"]["totalCount"] and repo["name"] not in repo_names:
                repos.append(repo)
                repo_names.add(repo["name"])
                releases.append(
                    {
                        "repo": repo["name"],
                        "release": repo["releases"]["nodes"][0]["name"]
                        .replace(repo["name"], "")
                        .strip(),
                        "published_at": repo["releases"]["nodes"][0][
                            "publishedAt"
                        ].split("T")[0],
                        "url": repo["releases"]["nodes"][0]["url"],
                    }
                )
        has_next_page = data["data"]["viewer"]["repositories"]["pageInfo"][
            "hasNextPage"
        ]
        after_cursor = data["data"]["viewer"]["repositories"]["pageInfo"]["endCursor"]
    return releases


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

releases = fetch_releases(TOKEN)
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
