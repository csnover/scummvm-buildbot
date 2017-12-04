from buildbot.locks import BaseLock, WorkerLock

class RealHostLock:
    def __init__(self, lockid):
        self.name = lockid.name
        self.max_count = lockid.maxCount
        self.max_count_for_host = lockid.maxCountForWorker
        self.description = "<HostLock(%s, %s, %s)>" % (self.name,
                                                       self.max_count,
                                                       self.max_count_for_host)
        self.locks = {}

    def __repr__(self):
        return self.description

    def getLock(self, worker):
        host_name = worker.worker_environ.get('WORKER_HOST', None)
        assert host_name is not None
        if host_name not in self.locks:
            max_count = self.max_count_for_host.get(host_name,
                                                    self.max_count)
            lock = self.locks[host_name] = BaseLock(self.name, max_count)
            desc = "<HostLock(%s, %s)[%s] %d>" % (self.name, max_count,
                                                  host_name, id(lock))
            lock.description = desc
            self.locks[host_name] = lock
        return self.locks[host_name]

class HostLock(WorkerLock):
    lockClass = RealHostLock

    def __init__(self, name, default_max=1, host_overrides=None):
        super(HostLock, self).__init__(name,
                                       maxCount=default_max,
                                       maxCountForWorker=host_overrides)
