from flask_frozen import Freezer
from sirikon_me.app import app

freezer = Freezer(app)

if __name__ == "__main__":
    freezer.freeze()
