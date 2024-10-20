from datetime import datetime, timezone

from flask import Flask, render_template

DOMAIN = "sirikon.me"
TITLE = "sirikon.me"

AUTHOR_NAME = "Carlos Fernández Llamas"
AUTHOR_EMAILS = ["hello@sirikon.me", "carlos@cojoneslargos.com"]

AUTHOR_MASTODON_SERVER = "mastodon.social"
AUTHOR_MASTODON_USER = "sirikon"
AUTHOR_MASTODON_URL = f"https://{AUTHOR_MASTODON_SERVER}/@{AUTHOR_MASTODON_USER}"

AUTHOR_POSITION = "Platform Engineer"
AUTHOR_EMPLOYER_NAME = "FeverUp.com"
AUTHOR_EMPLOYER_URL = "https://feverup.com"

AUTHOR_LINKEDIN_ID = "carlos-fernandez-llamas"

app = Flask(__name__)


@app.context_processor
def global_variables():
    return {
        "NOW": datetime.now(timezone.utc),
        "DOMAIN": DOMAIN,
        "TITLE": TITLE,
        "AUTHOR_NAME": AUTHOR_NAME,
        "AUTHOR_EMAILS": AUTHOR_EMAILS,
        "AUTHOR_MASTODON_SERVER": AUTHOR_MASTODON_SERVER,
        "AUTHOR_MASTODON_USER": AUTHOR_MASTODON_USER,
        "AUTHOR_MASTODON_URL": AUTHOR_MASTODON_URL,
        "AUTHOR_POSITION": AUTHOR_POSITION,
        "AUTHOR_EMPLOYER_NAME": AUTHOR_EMPLOYER_NAME,
        "AUTHOR_EMPLOYER_URL": AUTHOR_EMPLOYER_URL,
        "AUTHOR_LINKEDIN_ID": AUTHOR_LINKEDIN_ID,
    }


@app.template_filter("iso")
def iso_filter(d):
    return d.isoformat()


@app.template_filter("pad_post_number")
def pad_post_number_filter(n):
    return str(n).zfill(4)


@app.route("/")
def index():
    return render_template("index.html")


# import os
# import sys
# from pathlib import Path
# from datetime import datetime, timezone

# from staticjinja import Site

# from sirikon_me.posts import get_post, get_posts


# def index_context():
#     return {"posts": reversed(get_posts())}


# def post_context(template):
#     return {"post": get_post(template.name.removeprefix("posts/").removesuffix(".md"))}


# def atom_context():
#     return {"posts": reversed(get_posts())}


# def render_post(site, template, **kwargs):
#     out = site.outpath / Path(template.name).with_suffix(".html")
#     os.makedirs(out.parent, exist_ok=True)
#     site.get_template("_templates/post.html").stream(**kwargs).dump(
#         str(out), encoding="utf-8"
#     )


# def make_site():
#     return Site.make_site(
#         env_globals={
#             "NOW": datetime.now(timezone.utc),
#             "DOMAIN": DOMAIN,
#             "TITLE": TITLE,
#             "AUTHOR_NAME": AUTHOR_NAME,
#             "AUTHOR_EMAILS": AUTHOR_EMAILS,
#             "AUTHOR_MASTODON_SERVER": AUTHOR_MASTODON_SERVER,
#             "AUTHOR_MASTODON_USER": AUTHOR_MASTODON_USER,
#             "AUTHOR_MASTODON_URL": AUTHOR_MASTODON_URL,
#             "AUTHOR_POSITION": AUTHOR_POSITION,
#             "AUTHOR_EMPLOYER_NAME": AUTHOR_EMPLOYER_NAME,
#             "AUTHOR_EMPLOYER_URL": AUTHOR_EMPLOYER_URL,
#             "AUTHOR_LINKEDIN_ID": AUTHOR_LINKEDIN_ID,
#         },
#         searchpath="./src/website",
#         outpath="./output",
#         contexts=[
#             (r"index.html", index_context),
#             (r"atom.xml", atom_context),
#             (r".*\.md", post_context),
#         ],
#         rules=[(r"posts/.*\.md", render_post)],
#         filters={
#             "iso": lambda d: d.isoformat(),
#             "pad_post_number": lambda n: str(n).zfill(4),
#         },
#     )


# def cli():
#     args = sys.argv[1:]
#     if len(args) == 0:
#         print("Usage: python -m sirikon_me build/watch")
#         exit(1)
#     command = args[0]

#     site = make_site()

#     if command == "watch":
#         site.render(use_reloader=True)
#     elif command == "build":
#         site.render()
#     else:
#         print(f"Unknown command: {command}")
#         exit(1)


# cli()
