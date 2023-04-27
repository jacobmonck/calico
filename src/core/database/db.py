from os import environ

from databases import Database
from ormar import ModelMeta
from sqlalchemy import MetaData

database = Database(environ["DB_URI"])
metadata = MetaData()


class ParentMeta(ModelMeta):
    database = database
    metadata = metadata
