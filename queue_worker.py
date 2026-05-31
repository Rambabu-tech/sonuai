from redis import Redis
from rq import Worker, Queue

redis_conn = Redis.from_url("redis://localhost:6379")
queue = Queue("jobs", connection=redis_conn)

if __name__ == "__main__":
    worker = Worker([queue], connection=redis_conn)
    worker.work()