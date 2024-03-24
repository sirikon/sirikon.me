import re
from os import listdir
from os.path import join
from pathlib import Path
from dataclasses import dataclass
from html import escape

import markdown


@dataclass
class Post:
    number: str
    number_int: int
    date: str
    slug: str
    title: str
    content_html: str
    content_html_escaped: str


def get_post(slug):
    match = re.search(r"^([0-9]+)-", slug)
    if not match:
        return None

    number = match.group(1)
    file = join("./src/website/posts", slug + ".md")
    md = markdown.Markdown(
        output_format="html5", extensions=["extra", "meta", "codehilite"]
    )
    html = md.convert(Path(file).read_text())

    return Post(
        number=number,
        number_int=int(number),
        date=md.Meta["date"][0],
        slug=slug,
        title=md.Meta["title"][0],
        content_html=html,
        content_html_escaped=escape(html),
    )


def get_posts():
    slugs = list(
        reversed(sorted(f.removesuffix(".md") for f in listdir("./src/website/posts")))
    )

    posts: list[Post] = []

    for slug in slugs:
        post = get_post(slug)
        if post:
            posts.append(post)

    return sorted(posts, key=lambda p: p.number_int)
