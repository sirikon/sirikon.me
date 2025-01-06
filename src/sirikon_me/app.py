from datetime import datetime, timezone
from flask import Flask, render_template, Response
from sirikon_me.posts import get_post, get_posts

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

CACHE_BUSTER = int(datetime.now(timezone.utc).timestamp())

app = Flask(__name__)


@app.context_processor
def global_variables():
    return {
        "NOW": datetime.now(timezone.utc),
        "CACHE_BUSTER": CACHE_BUSTER,
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


@app.template_filter("post_number")
def post_number_filter(n):
    return str(n).zfill(4)


@app.template_filter("post_date")
def post_date_filter(d: datetime):
    return "-".join([str(d.year).zfill(4), str(d.month).zfill(2), str(d.day).zfill(2)])


@app.get("/")
def index():
    return render_template("index.html", posts=reversed(get_posts()))


@app.get("/about.html")
def about():
    return render_template("about.html")


@app.get("/not_found.html")
def not_found():
    return render_template("not_found.html")


@app.get("/posts/<post_slug>.html")
def post(post_slug: str):
    return render_template(
        "post.html",
        post=get_post(post_slug),
    )


@app.get("/atom.xml")
def atom():
    return Response(
        render_template("atom.xml", posts=reversed(get_posts())),
        content_type="application/xml",
    )
