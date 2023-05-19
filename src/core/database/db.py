from os import getenv

from databases import Database
from ormar import ModelMeta
from sqlalchemy import MetaData

database = Database(getenv("DB_URI", "postgresql://postgres:postgres@localhost/calico"))
metadata = MetaData()


class ParentMeta(ModelMeta):
    database = database
    metadata = metadata
