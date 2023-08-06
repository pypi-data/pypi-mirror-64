from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Rename the Django Project'

    def add_arguments(self, parser):
        # new name of the project
        parser.add_argument('new_project_name', type=str, help="The new project name (String)")
        # current name of the project
        parser.add_argument('--current_name',
                            default='boilerplate',
                            type=str,
                            help="The current project name (String)")

    def handle(self, *args, **options):
        new_name = options['new_project_name']
        current_name = options['current_name']

        # files that need to be update
        files = ['{}/settings/base_settings.py'.format(current_name),
                 '{}/wsgi.py'.format(current_name),
                 'manage.py']

        # folder that need to be update
        folder = current_name

        # update the files
        for file in files:
            with open(file, 'r') as f:
                file_data = f.read()    

            file_data = file_data.replace(current_name, new_name)

            with open(file, 'w') as f:
                f.write(file_data)

        # change name of the folder
        os.rename(folder, new_name)

        self.stdout.write(self.style.SUCCESS('Successfully updated the project name '
                                             'from "{}" to "{}"'.format(current_name, new_name)))

