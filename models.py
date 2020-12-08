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


'''

what is the weekly goal?

class WeekGoals(Model):
    job_seeker = FKF(User, backref=job)
    
    num_of_apps = IntegerField(default=0)
    apps_completed = IntegerField(default=0)
    incomplete_apps = IntegerField(default=0)

    class Meta:
        database=DATABASE


what are the stats for progress on each job?
class JobGoals(Model):
    job_seeker = FKF(User, backref=job)
    current_app = FKF(Job, backref=app)


'''


class Job(Model):
    company = CharField(max_length=60)
    position = CharField(max_length=100)
    location = CharField(max_length=60)
    link = CharField(max_length=100)
    materials_required = CharField(max_length=100)
    notes = CharField(default=None)
    applicant = ForeignKeyField(User, backref='jobs')
    created_at = DateTimeField(default=datetime.datetime.now)
    # status = IntegerField(default=1)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Job], safe=True)
    print("tables successfully created")
    DATABASE.close()
