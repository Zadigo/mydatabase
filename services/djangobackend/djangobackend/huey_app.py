import logging

import huey

logger = logging.getLogger(__name__)

huey_task = huey.RedisHuey('djangobackend')

@huey_task.periodic_task(huey.crontab(hour='*'))
def create_parquet_files():
    pass
