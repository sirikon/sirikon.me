import re
from os import listdir
from os.path import join
from pathlib import Path
from dataclasses import dataclass

import markdown


@dataclass
class Post:
    number: str
    number_int: int
    slug: str
    title: str
    content_html: str


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
        slug=slug,
        title=md.Meta["title"][0],
        content_html=html,
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
