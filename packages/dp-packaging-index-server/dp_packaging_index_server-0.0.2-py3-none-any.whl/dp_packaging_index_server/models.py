from django.db import models
from dp_file_system_file.models import FSFile


class Version(models.Model):

    version = models.CharField(max_length=255, blank=False, null=False)
    creation_date = models.DateTimeField(
        blank=True, null=True, auto_now_add=True)
    files = models.ManyToManyField(FSFile)


class Package(models.Model):

    name = models.CharField(max_length=255, blank=False, null=False)
    versions = models.ManyToManyField(Version, blank=True)

    creation_date = models.DateTimeField(
        blank=True, null=True, auto_now_add=True)
