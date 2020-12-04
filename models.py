from peewee import *
import datetime
from flask_login import UserMixin


DATABASE = SqliteDatabase('jobs.sqlite')


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE


"""
class Goals(Model):
    job_seeker = FKF(User, backref=job)
    current_app = FKF(Job, backref=app)
    time_spent = IntField(default=0)
    class Meta:
        database=DATABASE
"""


class Job(Model):
    company = CharField(max_length=60)
    position = CharField(max_length=100)
    location = CharField(max_length=60)
    link = CharField(max_length=100)
    materials_required = CharField(max_length=100)
    notes = CharField(default=None)
    applicant = ForeignKeyField(User, backref='jobs')
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Job], safe=True)
    print("tables successfully created")
    DATABASE.close()
