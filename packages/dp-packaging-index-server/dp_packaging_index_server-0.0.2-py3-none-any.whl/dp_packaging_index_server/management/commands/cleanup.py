import os
import shutil

from django.core.management.base import BaseCommand

from dp_file_system_file.models import FSFile

from dp_packaging_index_server.models import Package, Version
from dp_packaging_index_server.helper import UploadHelper


class Command(BaseCommand):
    help = 'Remove a package or all content from the server'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all', type=bool, default=False, help='Remove all packages from the server')
        parser.add_argument(
            '--package_name', action='append', help='Remove one or more packes from the server')

    def handle(self, *args, **options):

        base_path = UploadHelper().get_base_path()
        if options['all'] is True:

            FSFile.objects.all().delete()
            Version.objects.all().delete()
            Package.objects.all().delete()

            for folder_name in os.listdir(base_path):
                shutil.rmtree(os.path.join(base_path, folder_name))

            self.stdout.write(self.style.SUCCESS('All packages removed'))

        for package_name in options['package_name']:
            for object_package in Package.objects.filter(name=package_name):
                for object_version in object_package.versions.all():
                    for object_fs_file in object_version.files.all():
                        object_fs_file.delete()
                    object_version.delete()
                object_package.delete()
            shutil.rmtree(os.path.join(base_path, package_name))

            self.stdout.write(self.style.SUCCESS('Package ' + package_name))
