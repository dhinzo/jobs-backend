from peewee import *
import datetime
from flask_login import UserMixin
import os

from playhouse.db_url import connect


if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('jobs.sqlite')


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE


class Job(Model):
    company = CharField(max_length=60)
    position = CharField(max_length=100)
    location = CharField(max_length=60)
    link = CharField(max_length=100)
    materials_required = CharField(max_length=100)
    notes = CharField(default=None)
    applicant = ForeignKeyField(User, backref='jobs')
    created_at = DateTimeField(default=datetime.datetime.now)
    progress = CharField(default="unregistered")

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Job], safe=True)
    print("tables successfully created")
    DATABASE.close()
