from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.http import FileResponse

from .helper import UploadHelper

from .models import Package

from dp_file_system_file.models import FSFile


@csrf_exempt
@require_http_methods(["POST"])
def upload(request):
    if request.method == 'POST':
        upload_helper = UploadHelper()
        upload_helper.upload(request.FILES['content'])

    return HttpResponse()


@csrf_exempt
@require_http_methods(["GET"])
def index(request, name):
    base_url = 'http://localhost:8081/download/'
    a_tags = ''
    for object_package in Package.objects.filter(name=name):
        for object_version in object_package.versions.all():
            for object_fs_file in object_version.files.all():
                dict_ = {}
                dict_['url'] = base_url + object_fs_file.name
                dict_['name'] = object_fs_file.name

                a_tags += '<a href="{url}">{name}<a><br/>'.format(**dict_)

    html = '<html><body>{0}</body></html>'.format(a_tags)
    return HttpResponse(html)


@csrf_exempt
@require_http_methods(["GET"])
def download(request, name):
    objects = FSFile.objects.filter(name=name)
    if objects:
        object_fs_file = objects[0]
    else:
        object_fs_file = None

    response = FileResponse(open(object_fs_file.path, 'rb'))
    return response
