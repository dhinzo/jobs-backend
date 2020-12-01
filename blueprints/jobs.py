import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

# decorators
# first argument is blueprint's name
# second argument is the import name
job = Blueprint('jobs', 'job')


# GET route

@job.route('/', methods=["GET"])
def get_all_jobs():
    # find jobs and change each to a dictionary into a list
    try:
        jobs = [model_to_dict(job) for job in models.Job.select()]
        print(jobs)
        return jsonify(data=jobs, status={"code": 200, "message": "Successfuly got all jobs"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting all all job data"})


@job.route('/', methods=["POST"])
def create_job():
    try:
        payload = request.get_json()
        print(type(payload), 'payload')
        job = models.Job.create(**payload)
        # look at object data
        print(job.__dict__)
        # add print(dir(job)) if you want to see all the methods that you can use with job
        job_dict = model_to_dict(job)
        return jsonify(data=job_dict, status={"code": 200, "message": "Successfully created a job post"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "There was an error creating a job"})


@job.route('/<id>', methods=["PUT"])
def update_post(id):
    payload = request.get_json()
    query = models.Job.update(**payload).where(models.Job.id == id)
    query.execute()
    return jsonify(data=model_to_dict(models.Job.get_by_id(id)), status={"code": 200, "message": "Success updating"})


@job.route('/<id>', methods=["DELETE"])
def delete_job(id):
    delete_query = models.Job.delete().where(models.Job.id == id)
    num_of_rows_deleted = delete_query.execute()
    return jsonify(
        data={},
        message=f"Successfully deleted {num_of_rows_deleted} with the id {id}",
        status={"code": 200}
    )
