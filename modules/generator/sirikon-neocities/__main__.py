import os
from pathlib import Path
import re
import sys

from staticjinja import Site
import markdown


def get_post(slug):
    match = re.search(r"^([0-9]+)-", slug)
    if not match:
        return None

    number = match.group(1)
    file = os.path.join("./modules/website/posts", slug + ".md")
    md = markdown.Markdown(
        output_format="html5", extensions=["extra", "meta", "codehilite"]
    )
    html = md.convert(Path(file).read_text())
    return {"slug": slug, "number": number, "html": html, "meta": md.Meta}


def get_posts():
    slugs = list(
        reversed(
            sorted(f.removesuffix(".md") for f in os.listdir("./modules/website/posts"))
        )
    )

    posts = []

    for slug in slugs:
        post = get_post(slug)
        if post:
            posts.append(post)

    return posts


def index_context():
    return {"posts": get_posts()}


def post_context(template):
    return {"post": get_post(template.name.removeprefix("posts/").removesuffix(".md"))}


def render_post(site, template, **kwargs):
    out = site.outpath / Path(template.name).with_suffix(".html")
    os.makedirs(out.parent, exist_ok=True)
    site.get_template("_templates/post.html").stream(**kwargs).dump(
        str(out), encoding="utf-8"
    )


def make_site():
    return Site.make_site(
        searchpath="./modules/website",
        outpath="./output",
        contexts=[(r"index.html", index_context), (r".*\.md", post_context)],
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
