from django.test import TestCase
from django.test import override_settings
from dbschemas.models import DatabaseSchema

from dbschemas.tests.utils import DatabaseSchemaFactory

@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestFuncs(TestCase):
    def setUp(self):
        self.instance: DatabaseSchema = DatabaseSchemaFactory.create()

    def test_func_clean(self):
        pass

    def test_func_count(self):
        pass

    def test_func_sum(self):
        pass

    def test_func_avg(self):
        pass

    def test_func_min(self):
        pass

    def test_func_max(self):
        pass

    def test_func_upper(self):
        pass

    def test_func_lower(self):
        pass

    def test_func_title(self):
        pass

    def test_func_length(self):
        pass

    def test_func_trim(self):
        pass

    def test_func_group_concat(self):
        pass

    def test_func_coalesce(self):
        pass

    def test_func_extract(self):
        pass

    def test_func_now(self):
        pass

    def test_func_date(self):
        pass

    def test_func_time(self):
        pass

    def test_func_datetime(self):
        pass

    def test_func_strftime(self):
        pass

    def test_func_current_timestamp(self):
        pass

    def test_func_current_date(self):
        pass

    def test_func_current_time(self):
        pass

    def test_func_random(self):
        pass

    def test_func_md5(self):
        pass

    def test_func_sha256(self):
        pass

    def test_func_sha512(self):
        pass



class TestRelationships(TestCase):
    pass
