import os.path

from db.Db import Db
from query.Summarize import Summarize

if __name__ == '__main__':
    db = Db(os.path.abspath("../data"))
    db.load()

    summarize = Summarize(db)
    summarize.run()
