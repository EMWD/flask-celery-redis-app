from flask import Flask, redirect
from celery import Celery

app = Flask(__name__)

celery = Celery(
    'simple_worker',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)


@app.route('/')
def index():
    return redirect('/start')


@app.route('/start')
def call_method():
    app.logger.info("Invoking Method ")
    r = celery.send_task('tasks.longtime_add', kwargs={'param1': 2, 'param2': 2})
    app.logger.info(r.backend)
    return r.id


@app.route('/stat/<task_id>')
def get_status(task_id):
    status = celery.AsyncResult(task_id, app=celery)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)


@app.route('/res/<task_id>')
def task_result(task_id):
    result = celery.AsyncResult(task_id).result
    return "Task result " + str(result)
