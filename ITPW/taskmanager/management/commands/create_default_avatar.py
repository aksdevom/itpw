from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw
import os

class Command(BaseCommand):
    help = 'Creates default avatar image'

    def handle(self, *args, **options):
        from django.conf import settings
        
        path = os.path.join(settings.STATIC_ROOT, 'images', 'default-avatar.png')
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
            
        size = 200
        img = Image.new('RGB', (size, size), 'gray')
        draw = ImageDraw.Draw(img)
        draw.ellipse([40, 40, size-40, size-40], fill='white')
        img.save(path)
        
        self.stdout.write(self.style.SUCCESS('Successfully created default avatar'))
