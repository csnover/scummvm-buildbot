from buildbot.plugins import worker
Worker = worker.Worker

def make_workers(worker_names, secrets):
    return [Worker(name, password=secrets["worker_password"]) for name in worker_names]
