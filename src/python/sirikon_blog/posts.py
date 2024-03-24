import re
from os import listdir
from os.path import join
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timezone

import markdown

POSTS_PATH = "src/website/posts"
POST_SLUG_REGEXP = r"^([0-9]+)-.+"


@dataclass
class Post:
    slug: str
    number: int
    title: str
    date: datetime
    content_html: str


def get_post(slug):
    number = int(re.match(POST_SLUG_REGEXP, slug).group(1))
    post_file = join(POSTS_PATH, slug + ".md")
    md = markdown.Markdown(
        output_format="html5", extensions=["extra", "meta", "codehilite"]
    )
    html = md.convert(Path(post_file).read_text())

    return Post(
        slug=slug,
        number=number,
        title=md.Meta["title"][0],
        date=datetime.strptime(md.Meta["date"][0], "%Y-%m-%d %H:%M").replace(
            tzinfo=timezone.utc
        ),
        content_html=html,
    )


def get_posts():
    return sorted(
        [get_post(slug) for slug in _get_posts_slugs()], key=lambda p: p.number
    )


def _get_posts_slugs():
    return [
        f.removesuffix(".md")
        for f in listdir(POSTS_PATH)
        if re.match(POST_SLUG_REGEXP, f)
    ]
