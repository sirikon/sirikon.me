import sys
from staticjinja import Site

site = Site.make_site(searchpath="./modules/website", outpath="./output")
site.render(use_reloader=sys.argv[1] == "watch")
