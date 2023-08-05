import os
import shutil
import tempfile

from pkginfo import SDist, Wheel

from dp_settings.models import DpSettings
from .apps import Config

from .models import Version, Package

from dp_file_system_file.models import FSFile


class UploadHelper:

    def get_base_path(self):

        objects = DpSettings.objects.filter(
            app_name=Config.name,
            key=Config.ask_package_storage_path)

        if len(objects):
            base_path = objects[0].value_string
            if not base_path.endswith(os.sep):
                base_path += os.sep
            return base_path

    def create_full_path(self, package_name, version, file_name):

        path = self.get_base_path()

        path += package_name
        path += os.sep
        path += version
        path += os.sep
        path += file_name

        return path

    def upload(self, file):

        # InMemoryUploadedFile

        file_name = file.name

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_name)
        for line in file:
            temp_file.write(line)
        temp_file.close()

        if file_name.endswith('whl'):
            package = Wheel(temp_file.name)
        else:
            package = SDist(temp_file.name)

        objects = Package.objects.filter(name=package.name)
        if len(objects):
            object_package = objects[0]
        else:
            object_package = Package.objects.create(name=package.name)
            object_package.save()

        objects = Version.objects.filter(
            version=package.version,
            package__name=package.name)
        if len(objects):
            object_version = objects[0]
        else:
            object_version = Version.objects.create(version=package.version)
            object_package.versions.add(object_version)
            object_package.save()
            object_version.save()

        # Version update is allowed
        objects = FSFile.objects.filter(name=file_name)
        if objects:
            object_fs_file = objects[0]
        else:
            object_fs_file = FSFile.objects.create(
                name=file_name,
                mime_type=file.content_type,
                size=file.size
            )
            object_version.files.add(object_fs_file)
            object_version.save()

        file_path = self.create_full_path(
            package.name,
            package.version,
            file_name)

        directory_path = os.path.dirname(file_path)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        object_fs_file.path = file_path
        object_fs_file.save()

        if os.path.exists(file_path):
            os.remove(file_path)

        shutil.move(temp_file.name, file_path)
