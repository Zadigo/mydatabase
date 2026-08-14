# import pytest
# from django.test import override_settings

# from tabledocuments import tasks
# from tabledocuments.models import TableDocument
# from tabledocuments.tests.utils import DocumentFactory


# @pytest.fixture
# def tabledoc() -> TableDocument:
#     return DocumentFactory.create()


# @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
# @pytest.mark.django_db
# def test_update_document_options(tabledoc):
#     result = tasks.update_document_options(tabledoc.document_uuid)

import pytest
from pytest_celery import (
    CeleryBrokerCluster,
    CeleryTestSetup,
    RabbitMQTestBroker,
    RedisTestBroker,
)

from tabledocuments.models import TableDocument
from tabledocuments.tests.utils import DocumentFactory


@pytest.fixture
def tabledoc() -> TableDocument:
    return DocumentFactory.create()



@pytest.fixture
def celery_broker_cluster(celery_rabbitmq_broker: RabbitMQTestBroker) -> CeleryBrokerCluster:
    cluster = CeleryBrokerCluster(celery_rabbitmq_broker)
    yield cluster
    cluster.teardown()


@pytest.fixture
def celery_backend_cluster(celery_redis_broker: RedisTestBroker) -> CeleryBrokerCluster:
    cluster = CeleryBrokerCluster(celery_redis_broker)
    yield cluster
    cluster.teardown()


@pytest.fixture
def default_worker_tasks(default_worker_tasks: set) -> set:
    from tabledocuments import tasks

    default_worker_tasks.add(tasks)
    return default_worker_tasks


def test_update_document_options(celery_setup: CeleryTestSetup, tabledoc):
    from tabledocuments import tasks

    assert isinstance(celery_setup.broker, RabbitMQTestBroker)
    assert isinstance(celery_setup.backend, RedisTestBroker)
    assert tasks.update_document_options.apply_async(
        args=[
            tabledoc.document_uuid
        ]
    )
