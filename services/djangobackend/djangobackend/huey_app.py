import logging

import huey

# huey_consumer djangobackend.huey_app.huey_task -w 4

logger = logging.getLogger(__name__)

huey_task = huey.RedisHuey('djangobackend')

@huey_task.periodic_task(huey.crontab(hour='*'))
def check_endpoints():
    pass
