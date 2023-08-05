import os
import base64
import mimetypes

from django.test import Client, RequestFactory
from django.test import TestCase
from django.contrib.auth.models import User
from django.http import HttpResponse

from dp_settings.models import DpSettings

from .models import Version, Package
from .helper import UploadHelper
from .apps import Config
from .middleware import BasicAuthMiddleware

from dp_file_system_file.models import FSFile

mimetypes.add_type('application/octet-stream', '.whl')


class TestCases(TestCase):

    base_path = os.path.join('tmp', 'packages') + os.path.sep
    package_name = 'dp-test-app1'
    username = password = 'test'
    email = 'test@test.de'

    def setUp(self):

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password)

        # Add App config to Database
        object_ = DpSettings.objects.create()
        object_.app_name = Config.name
        object_.key = Config.ask_package_storage_path
        object_.value_string = self.base_path
        object_.save()

    def test_001(self):

        # Test create package and two Versions (Model Test).
        object_test_package = Package.objects.create(name=self.package_name)
        object_version_1 = Version.objects.create(version='0.0.1')
        object_version_2 = Version.objects.create(version='0.0.2')

        object_test_package.versions.add(object_version_1)
        object_test_package.versions.add(object_version_2)
        object_test_package.save()

        objects_versions = object_test_package.versions.all()
        self.assertEqual(len(objects_versions), 2)

    def test_002(self):

        # Repository Base Path storage test.
        self.assertEqual(UploadHelper().get_base_path(), self.base_path)

    def test_003(self):

        # Full path test.
        file_name = 'dp_test_app1-0.0.2-py3-none-any.whl'
        path_generated = UploadHelper().create_full_path(
            self.package_name, '0.0.2', file_name)
        path_expected = self.base_path + self.package_name + \
            os.sep + '0.0.2' + os.sep + file_name

        self.assertEqual(path_generated, path_expected)

    def test_004(self):

        # Upload and Download Test
        directory = os.path.dirname(__file__)
        directory = os.path.join(directory, 'tests', 'files')
        for file_name in os.listdir(directory):
            path = os.path.join(directory, file_name)
            with open(path, 'rb') as fp:
                data = {'content': fp}
                upload_form = Client()
                upload_form.login(username=self.username, password=self.email)
                upload_form.post('/upload', data)

            object_fsfile = FSFile.objects.filter(name=file_name)[0]

            self.assertEqual(object_fsfile.name, file_name)

            object_version = Version.objects.filter(
                files__id=object_fsfile.id)[0]
            object_package = Package.objects.filter(
                versions__id=object_version.id)[0]

            response = Client().get('/index/'+object_package.name+'/')

            self.assertEqual(str(response.content).count(file_name), 2)

            path = os.path.join(directory, file_name)

            response = Client().get('/download/'+file_name+'/')
            data_response = b"".join(response.streaming_content)
            self.assertEqual(open(path, 'rb').read(), data_response)

    def test_005(self):

        # Middleware Test
        def get_response(request):
            return HttpResponse("fake")

        request = RequestFactory()
        request.META = {
            "REQUEST_METHOD": "POST",
            "HTTP_APP_VERSION": "1.0.0",
            "HTTP_USER_AGENT": "AUTOMATED TEST"
        }
        request.path = '/testURL/'
        request.session = self.client.session
        request.session.create()
        request.user = None
        # TODO
        request.META['HTTP_AUTHORIZATION'] = 'Basic ' + \
            base64.b64encode(b'test:test').strip().decode('ascii')
        middleware = BasicAuthMiddleware(get_response)
        middleware(request)

        self.assertEqual(request.user.is_authenticated, True)
