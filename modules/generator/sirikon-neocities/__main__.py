import sys
from staticjinja import Site


site = Site.make_site(searchpath="./modules/website", outpath="./output")


args = sys.argv[1:]
if len(args) == 0:
    print("Usage: python -m sirikon-neocities build/watch")
    exit(1)
command = args[0]

if command == "watch":
    site.render(use_reloader=True)
elif command == "build":
    site.render()
else:
    print(f"Unknown command: {command}")
    exit(1)
