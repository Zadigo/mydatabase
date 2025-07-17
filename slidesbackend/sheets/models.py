import pathlib

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from sheets.utils import create_file_name, create_id
from sheets.validators import validate_id

USER_MODEL = get_user_model()


class Webhook(models.Model):
    """A webhook is an endpoint via which
    data can be updated or added in a sheet"""

    sheet = models.ForeignKey(
        'Sheet',
        on_delete=models.CASCADE,
        blank=True
    )
    webhook_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        validators=[validate_id]
    )
    usage = models.PositiveIntegerField(default=0)
    last_usage = models.DateTimeField(
        default=now
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        constraints = [
            models.UniqueConstraint(
                fields=['webhook_id', 'sheet'],
                name='unique_webhook_id'
            )
        ]

    def __str__(self):
        return f'Webhook: {self.webhook_id}'


class Sheet(models.Model):
    """A sheet is a connection to a csv file
    or a Google Sheet spreadsheet. A sheet can
    be created either by uploading a csv file,
    by creating a csv file via an API endpoint or
    by linking to a Google spreadsheet"""

    user = models.ForeignKey(USER_MODEL, models.CASCADE)
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    sheet_id = models.CharField(
        verbose_name='Sheet ID',
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        validators=[validate_id]
    )
    url = models.URLField(
        verbose_name='URL',
        unique=True,
        help_text=_("The Google sheet's url"),
        blank=True,
        null=True
    )
    csv_file = models.FileField(
        verbose_name='CSV file',
        help_text=_("The csv file to use to create a new sheet"),
        upload_to=create_file_name,
        blank=True,
        null=True
    )
    endpoint_url = models.URLField(
        help_text=_("The endpoint to use to create a new sheet"),
        blank=True,
        null=True
    )
    endpoint_data_key = models.CharField(
        max_length=100,
        help_text=_("The key under which the data is stored"),
        blank=True,
        null=True
    )
    columns = models.JSONField(
        help_text=_("Available columns in the data source"),
        blank=True,
        null=True
    )
    column_types = models.JSONField(
        help_text=_("The data type for each column"),
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Sheet: {self.sheet_id}'

    def clean(self):
        return super().clean()

    @property
    def csv_based(self):
        """Returns whether the sheet is a
        csv based one aka started by uploading
        a csv file"""
        return self.csv_file is not None

    @property
    def is_endpoint(self):
        return self.endpoint_url != None


@receiver(pre_save, sender=Sheet)
def create_sheet_id(instance, **kwargs):
    if instance.sheet_id is None:
        instance.sheet_id = create_id('sh')


@receiver(pre_save, sender=Webhook)
def create_webhook_id(instance, **kwargs):
    if instance.webhook_id is None:
        instance.webhook_id = create_id('wk')


@receiver(post_delete, sender=Sheet)
def delete_csv_file_on_delete(instance, **kwargs):
    """Deletes a csv file that was previously uploaded
    by a user once the instance is deleted"""
    if instance.csv_file is not None:
        try:
            path = pathlib.Path(instance.csv_file.path)
        except:
            return
        if path.exists() and path.is_file():
            path.unlink()


@receiver(pre_save, sender=Sheet)
def change_csv_file_on_delete(instance, **kwargs):
    """Checks if a file is the same as the current
    one saved in the database and deletes the old file
    to replace it by the new uploaded one if needed"""
    if instance.pk:
        try:
            user_sheet = Sheet.objects.get(user__id=instance.pk)
        except:
            return

        if user_sheet and user_sheet.csv_file == instance.csv_file:
            try:
                path = user_sheet.csv_file.path
            except:
                return

            path = pathlib.Path(path)
            if path.exists() and path.is_file():
                path.unlink()


@receiver(post_save, sender=Sheet)
def clean_csv_data(instance, **kwargs):
    # Work the CSV file based on the elemnents
    # that the user has provided to us
    # csv_instance = CSVData(instance)
    # print(csv_instance)
    pass
