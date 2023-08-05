from django.core.management.base import BaseCommand
from dp_settings.models import AppSettings
from dp_packaging_index_server.apps import Config


class Command(BaseCommand):
    help = 'Set the base storage path for the packages'
    argument_name = Config.ask_package_storage_path

    def add_arguments(self, parser):
        parser.add_argument('--'+self.argument_name, help=self.help)

    def handle(self, *args, **options):

        objects = AppSettings.objects.filter(
            app_name=Config.name,
            key=Config.ask_package_storage_path)

        if len(objects):
            object_ = objects[0]

        object_ = AppSettings.objects.create()
        object_.app_name = Config.name
        object_.key = Config.ask_package_storage_path
        object_.value_string = options[self.argument_name]
        object_.save()

        self.stdout.write(self.style.SUCCESS('Path successfully set.'))
