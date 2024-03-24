import os
import sys
from pathlib import Path
from datetime import datetime, timezone

from staticjinja import Site
from feedgen.feed import FeedGenerator

from sirikon_blog.posts import get_post, get_posts

DOMAIN = "sirikon.neocities.org"

date_zero = datetime.fromtimestamp(0, timezone.utc)


def index_context():
    return {"posts": reversed(get_posts())}


def post_context(template):
    return {"post": get_post(template.name.removeprefix("posts/").removesuffix(".md"))}


def atom_context():
    fg = FeedGenerator()
    fg.id(f"https://{DOMAIN}")
    print(date_zero)
    # fg.updated(date_zero)
    fg.title("Sirikon's Neocities")
    fg.author({"name": "Carlos Fdez. Llamas", "email": "hello@sirikon.me"})
    fg.language("en")

    posts = get_posts()
    for post in posts:
        fe = fg.add_entry()
        fe.id(f"https://{DOMAIN}/posts/{post.slug}")
        # fe.updated(date_zero)
        fe.title(post.title)
        fe.content(post.content_html, type="html")

    return {"content": fg.atom_str(pretty=True).decode()}


def render_post(site, template, **kwargs):
    out = site.outpath / Path(template.name).with_suffix(".html")
    os.makedirs(out.parent, exist_ok=True)
    site.get_template("_templates/post.html").stream(**kwargs).dump(
        str(out), encoding="utf-8"
    )


def make_site():
    return Site.make_site(
        searchpath="./src/website",
        outpath="./output",
        contexts=[
            (r"index.html", index_context),
            (r"atom.xml", atom_context),
            (r".*\.md", post_context),
        ],
        rules=[(r"posts/.*\.md", render_post)],
    )


def cli():
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python -m sirikon-neocities build/watch")
        exit(1)
    command = args[0]

    site = make_site()

    if command == "watch":
        site.render(use_reloader=True)
    elif command == "build":
        site.render()
    else:
        print(f"Unknown command: {command}")
        exit(1)


cli()
