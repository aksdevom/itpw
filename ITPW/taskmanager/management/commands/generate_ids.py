from django.core.management.base import BaseCommand
from taskmanager.models import Project, Task

class Command(BaseCommand):
    help = 'Generates project_id and task_id for existing records'

    def handle(self, *args, **kwargs):
        # Generate Project IDs
        for index, project in enumerate(Project.objects.filter(project_id__isnull=True), 1):
            project.project_id = f'PROJ-{str(index).zfill(3)}'
            project.save()
            
        # Generate Task IDs
        for project in Project.objects.all():
            for index, task in enumerate(Task.objects.filter(project=project, task_id__isnull=True), 1):
                task.task_id = f'{project.project_id}-T{str(index).zfill(3)}'
                task.save()

        self.stdout.write(self.style.SUCCESS('Successfully generated all IDs'))
